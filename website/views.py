from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from .utils import gpt, whisper, audioconvert
from .models import FormTemplate, User, Question, Form, FormResponse, FormConfig, FormConfig
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, login
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.
def index(request):
    if request.method == 'POST':
        login_value = request.POST.get('email')
        password = request.POST.get('password')

        # Case-insensitive lookup for email
        user = User.objects.filter(email__iexact=login_value).first()

        if user is None:
            # Case-insensitive lookup for username
            user = User.objects.filter(username__iexact=login_value).first()

        if user is not None and user.check_password(password):
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect username or password.')
            return redirect('index')
    else:
        return render(request, 'index.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email address')
            return redirect('signup')

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, ', '.join(e.messages))
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('signup')
        
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)

        # Automatically sign in the user
        login(request, user)

        messages.success(request, 'Account Created. Create a new form template by clicking + at the bottom of the page.')
        return redirect('dashboard')

    return render(request, 'signup.html')

@login_required
def usersettings(request):
    if request.method == 'POST':
        # Handle the form submission (change password)
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # To maintain the user's session
            messages.success(request, 'Your password was successfully changed.')
            return redirect('usersettings')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'usersettings.html', {'form': form})


@login_required
def editform(request, form_template_id):
    form_template = get_object_or_404(FormTemplate, id=form_template_id)
    if form_template.user != request.user: # Only the forms attached to the user can be accessed
        return HttpResponseForbidden("You don't have permission to access this form.")

    questions = Question.objects.filter(template=form_template)
    form_config = form_template.formconfig

    question_list = []
    for question in questions:
        question_list.append(question.question)

    return render(request, 'editform.html', {'form_template': form_template, 'questions': question_list, 'form_config': form_config})

@login_required
def delete_account(request):
    if request.method == 'POST':
        try:
            password = request.POST.get('password')
            user = request.user
            if user.check_password(password):
                # Delete the account
                user.delete()
                messages.success(request, 'Your account has been deleted.')
                return redirect('index')  # Redirect to the desired page after account deletion
            else:
                messages.error(request, 'Invalid password. Please try again.')
        except Exception as e:
            messages.error(request, f'Error in creating question: {str(e)}')
            return JsonResponse({'success': False})

    return redirect('usersettings')  # Redirect back to the user settings page


@login_required
def dashboard(request):
    form_templates = FormTemplate.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'form_templates': form_templates})

@login_required
def create_default_form_template(request):
    try:
        if request.method == 'POST':
            user = request.user

            # Check if the user has approval and fewer than 3 form templates
            if user.approval or FormTemplate.objects.filter(user=user).count() < 3:
                title = 'Untitled Form'
                body = 'Form description'
                form_template = FormTemplate.objects.create(title=title, body=body, user=user)

                # Create a Settings instance and attach it to the form_template
                FormConfig.objects.create(
                    form_template=form_template,
                    conversation_type='A Medical Visit Between a Patient and Doctor',
                    system_prompt='''You are WhichDoctor AI, a medical assistant for a doctor processing inbound patients. Your goal is to help process the conversation and fill out the provided form query.
                    - The dialogue you are provided will consist of a conversation between a doctor and a patient.
                    - You will take this information provided and fill out the following form and write "N/A" if you do not have information to factually fill out the questions or interpret responses.
                    - You may interpret answers to the questions only using factual information stated in the transcript, do not fabricate any information.
                    - You will answer each question factually, as if you were filling out a form, and refrain from adding any additional commentary.
                    - You will only answer the question and not write anything else. If you need more information or cannot give a factual answer, write "N/A".''',
                )

                # Redirect the user to the newly created form template
                messages.success(request, 'Form Template Created. Create a new question by clicking + at the bottom of the page.')
                return redirect('editform', form_template_id=form_template.id)
            else:
                messages.error(request, "Non-whitelisted accounts have a maximum of 3 form templates. Delete a form template or request whitelisted access to create a new form.")
                return redirect('dashboard')
    except Exception as e:
        messages.error(request, f'Error in creating form template: {str(e)}')
        return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'dashboard.html')

@login_required
def delete_form_template(request, form_template_id):
    try:
        form_template = get_object_or_404(FormTemplate, id=form_template_id)
        if form_template.user != request.user:
            return HttpResponseForbidden("You don't have permission to delete this form template.")

        if request.method == 'POST':
            form_template.delete()
            return redirect('dashboard')
        
    except Exception as e:
        messages.error(request, f'Error in deleting form template: {str(e)}')
        return JsonResponse({'success': False})
    
    return HttpResponseBadRequest("Invalid request method.")

@login_required
def edit_template_title(request, form_template_id):
    form_template = get_object_or_404(FormTemplate, id=form_template_id)
    if form_template.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this form.")

    questions = Question.objects.filter(template=form_template)
    form_config = form_template.formconfig

    question_list = []
    for question in questions:
        question_list.append(question.question)

    return render(request, 'editform.html', {'form_template': form_template, 'editing_title': True, 'questions': question_list, 'form_config': form_config})

@login_required
def save_template_title(request, form_template_id):
    try:
        form_template = get_object_or_404(FormTemplate, id=form_template_id)
        if form_template.user != request.user:
            return HttpResponseForbidden("You don't have permission to save this form.")

        if request.method == 'POST':
            form_template.title = request.POST.get('title')
            form_template.save()

            questions = Question.objects.filter(template=form_template)
            form_config = form_template.formconfig

            question_list = []
            for question in questions:
                question_list.append(question.question)
            return render(request, 'editform.html', {'form_template': form_template, 'editing_title': False, 'questions': question_list, 'form_config': form_config})
            
    except Exception as e:
        messages.error(request, f'Error in saving template title: {str(e)}')
        return JsonResponse({'success': False})
    
    return HttpResponseBadRequest("Invalid request method.")

@login_required
def edit_template_body(request, form_template_id):
    form_template = get_object_or_404(FormTemplate, id=form_template_id)
    if form_template.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this form.")
    
    questions = Question.objects.filter(template=form_template)
    form_config = form_template.formconfig

    question_list = []
    for question in questions:
        question_list.append(question.question)

    return render(request, 'editform.html', {'form_template': form_template, 'editing_body': True, 'questions': question_list, 'form_config': form_config})

@login_required
def save_template_body(request, form_template_id):
    try:
        form_template = get_object_or_404(FormTemplate, id=form_template_id)
        if form_template.user != request.user:
            return HttpResponseForbidden("You don't have permission to save this form.")

        if request.method == 'POST':
            form_template.body = request.POST.get('body')
            form_template.save()

            questions = Question.objects.filter(template=form_template)
            form_config = form_template.formconfig

            question_list = []
            for question in questions:
                question_list.append(question.question)
            
            return render(request, 'editform.html', {'form_template': form_template, 'editing_body': False, 'questions': question_list, 'form_config': form_config})
            
    except Exception as e:
        messages.error(request, f'Error in saving template description: {str(e)}')
        return JsonResponse({'success': False})
    
    return HttpResponseBadRequest("Invalid request method.")

def save_form_config(request, form_template_id):
    if request.method == 'POST':
        try:
            form_template = get_object_or_404(FormTemplate, id=form_template_id)
            form_config = form_template.formconfig

            form_config.language = request.POST.get('language')
            form_config.conversation_type = request.POST.get('conversation_type')
            form_config.audio_recognition_model_id = request.POST.get('audio_recognition_model_id')
            form_config.system_prompt = request.POST.get('system_prompt')
            form_config.ai_model_id = request.POST.get('ai_model_id')
            form_config.temperature = request.POST.get('temperature')
            form_config.presence_penalty = request.POST.get('presence_penalty')

            form_config.save()

        except Exception as e:
            messages.error(request, f'Error in saving form config: {str(e)}')
            return JsonResponse({'success': False})

    return redirect('editform', form_template_id=form_template_id)

@login_required
def create_question(request, form_template_id):
    if request.method == 'POST':
        try:
            user = request.user
            template = get_object_or_404(FormTemplate, id=form_template_id)

            # Check if the user has approval and fewer than 3 questions in the form template
            if user.approval or Question.objects.filter(template=template).count() < 3:
                title = 'New Question'
                Question.objects.create(template=template, question=title)
                return redirect('editform', form_template_id=form_template_id)
            else:
                messages.error(request, "Non-whitelisted accounts have a maximum of 3 questions per form template.")
                return redirect('editform', form_template_id=form_template_id)
        
        except Exception as e:
            messages.error(request, f'Error in creating question: {str(e)}')
            return JsonResponse({'success': False})

    return redirect('editform', form_template_id=form_template_id)

@login_required
def edit_question(request, form_template_id, question_id):
    try:
        question = get_object_or_404(Question, id=question_id)
        form_template = get_object_or_404(FormTemplate, id=form_template_id)
        if form_template.user != request.user:
            return HttpResponseForbidden("You don't have permission to edit this form.")

        if request.method == 'POST':
            question.question = request.POST.get('question')
            question.save()
            return redirect('editform', form_template_id=form_template.id)

        # Set editing mode for the current question
        question.editing = True
        question.save()

    except Exception as e:
        messages.error(request, f'Error in editing question: {str(e)}')
        return JsonResponse({'success': False})
    
    questions = Question.objects.filter(template=form_template)
    form_config = form_template.formconfig

    question_list = []
    for question in questions:
        question_list.append(question.question)
    
    return render(request, 'editform.html', {'form_template': form_template, 'question': question, 'editing': True, 'questions': question_list, 'form_config': form_config})

@login_required
def save_question(request, form_template_id, question_id):
    try:
        question = get_object_or_404(Question, id=question_id)
        form_template = get_object_or_404(FormTemplate, id=form_template_id)
        if form_template.user != request.user:
            return HttpResponseForbidden("You don't have permission to save this form.")

        if request.method == 'POST':
            question.question = request.POST.get('question')
            question.editing = False
            question.save()
            return redirect('editform', form_template_id=form_template.id)

    except Exception as e:
        messages.error(request, f'Error in saving question: {str(e)}')
        return JsonResponse({'success': False})

    return HttpResponseBadRequest("Invalid request method.")

@login_required
def delete_question(request, form_template_id, question_id):
    try:
        question = get_object_or_404(Question, id=question_id)
        form_template = get_object_or_404(FormTemplate, id=form_template_id)
        if form_template.user != request.user:
            return HttpResponseForbidden("You don't have permission to delete this question.")

        if request.method == 'POST':
            question.delete()
            return redirect('editform', form_template_id=form_template.id)
    except Exception as e:
        messages.error(request, f'Error in deleting question: {str(e)}')
        return JsonResponse({'success': False})

    return HttpResponseBadRequest("Invalid request method.")

@login_required
def create_form(request, template_id):
    form_template = get_object_or_404(FormTemplate, id=template_id)
    user = request.user

    # Check if the user has unlimited forms due to approval
    try:
        if user.approval:
            # Create a new Form linked to the template and the user
            form = Form.objects.create(template=form_template, user=user)
        else:
            # Check if the user has reached the maximum number of forms per day
            today = timezone.now().date()
            form_count = Form.objects.filter(user=user, created_at__date=today).count()
            if form_count >= 3:
                reset_time = datetime.combine(today + timedelta(days=1), datetime.min.time())  # Reset time is set to midnight of the next day
                time_left = reset_time - datetime.now()

                # Format the time left to display only hours, minutes, and seconds
                hours = int(time_left.total_seconds() // 3600)
                minutes = int((time_left.total_seconds() % 3600) // 60)
                seconds = int(time_left.total_seconds() % 60)
                time_left_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                messages.error(request, f"You have reached the maximum number of form responses allowed for today. Time left: {time_left_str}")
                return redirect('dashboard')

            # Create a new Form linked to the template and the user
            form = Form.objects.create(template=form_template, user=user)

        # Retrieve all the questions associated with the template
        questions = Question.objects.filter(template=form_template)

        # Create a FormResponse for each question
        for question in questions:
            FormResponse.objects.create(form=form, question=question)

        responses = FormResponse.objects.filter(form=form)
        # Redirect to the newly created form's page or render a success message
        # redirect to record form
    except Exception as e:
        messages.error(request, f'Error in creating form: {str(e)}')
        return JsonResponse({'success': False})

    return render(request, 'record.html', {'form': form, 'responses': responses, 'form_template': form_template})



@login_required
def upload_audio(request, form_id):
    if request.method == 'POST':
        form_instance = get_object_or_404(Form, id=form_id)
        audio_chunk = request.FILES.get('audioChunk')  # Get the uploaded audio file
        if audio_chunk:
            form_instance.audio_file.save(audio_chunk.name, audio_chunk)
            audio_bytes = audio_chunk.read()
            transcribed_text = whisper.convert_audio(audio_bytes, form_instance)
            form_instance.transcript = transcribed_text
            form_instance.save()
        return JsonResponse({'success': True})
    return HttpResponse('ok')

@login_required
def stop_audio(request, form_id):
    if request.method == 'POST':
        form_instance = get_object_or_404(Form, id=form_id)
        audio_chunk = request.FILES.get('audioChunk')  # Get the uploaded audio file
        print(request.POST.get('dataType'))
        if audio_chunk:
            audio_bytes = audio_chunk.read()
            try:
                if request.POST.get('dataType') == 'mp4':
                    converted_audio_bytes = audioconvert.mp4_to_webm(audio_bytes)
                    transcribed_text = whisper.convert_audio(converted_audio_bytes, form_instance)
                else:
                    transcribed_text = whisper.convert_audio(audio_bytes, form_instance)
                form_instance.transcript = transcribed_text
                form_instance.save()
            except Exception as e:
                messages.error(request, f'Error in transcribing audio: {str(e)}')
                return JsonResponse({'success': False})
            
        form_responses = form_instance.formresponse_set.all()
        for form_response in form_responses:
            try:
                gpt.process_form_query(form_response)
            except Exception as e:
                messages.error(request, f'Error processing form query: {str(e)}')
                return JsonResponse({'success': False})

        return JsonResponse({'success': True})
        
    return JsonResponse({'success': False})

@login_required
def response_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    # Have a setting to make form data public
    if form.user != request.user: # Only the forms attached to the user can be accessed
        return HttpResponseForbidden("You don't have permission to access this form.")

    form_responses = form.formresponse_set.all()

    return render(request, 'responseform.html', {'form': form, 'responses': form_responses})