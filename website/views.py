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
from django.contrib.auth import update_session_auth_hash

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
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('index')

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

    question_list = []
    for question in questions:
        question_list.append(question.question)

    return render(request, 'editform.html', {'form_template': form_template, 'questions': question_list})

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = request.user
        if user.check_password(password):
            # Delete the account
            user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('index')  # Redirect to the desired page after account deletion
        else:
            messages.error(request, 'Invalid password. Please try again.')

    return redirect('usersettings')  # Redirect back to the user settings page


@login_required
def dashboard(request):
    form_templates = FormTemplate.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'form_templates': form_templates})

@login_required
def create_default_form_template(request):
    if request.method == 'POST':
        title = 'Untitled Form'
        body = 'Form description'
        user = request.user
        form_template = FormTemplate.objects.create(title=title, body=body, user=user)\
        
        # Create a Settings instance and attach it to the form_template, this is tailored towards medical but perhaps the user can select the default template type when they create in the future
        FormConfig.objects.create(
            form_template=form_template,
            conversation_type='A Medical Visit Between a Patient and Doctor',
            system_prompt='''You are WhichDoctor AI, a medical assistant for a doctor processing inbound patients. Your goal is to help process the conversation and fill out the provided form query.
            - The dialogue you are provided will consist of a conversation between a doctor and a patient.
            - You will take this information provided and fill out the following form and write "N/A" if you do not have information to factually fill out the questions or interpret responses.
            - You may interpret answers to the questions only using factual information stated in the transcript, do not fabricate any information.
            - You will answer each question factually, as if you were filling out a form, and refrain from adding any additional commentary.
            - You will only answer the question and not write anything else. If you need more information or can not give a factual answer, write "N/A".''',
        )

        return redirect('dashboard')
    return render(request, 'dashboard.html')

@login_required
def edit_template_title(request, form_template_id):
    form_template = get_object_or_404(FormTemplate, id=form_template_id)
    if form_template.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this form.")

    return render(request, 'editform.html', {'form_template': form_template, 'editing': True})

@login_required
def save_template_title(request, form_template_id):
    form_template = get_object_or_404(FormTemplate, id=form_template_id)
    if form_template.user != request.user:
        return HttpResponseForbidden("You don't have permission to save this form.")

    if request.method == 'POST':
        form_template.title = request.POST.get('title')
        form_template.save()
        return redirect('editform', form_template_id=form_template.id)

    return HttpResponseBadRequest("Invalid request method.")

@login_required
def create_question(request, form_template_id):
    if request.method == 'POST':
        title = 'New Question'
        template = get_object_or_404(FormTemplate, id=form_template_id)
        Question.objects.create(template=template, question=title)
        return redirect('editform', form_template_id=form_template_id)
    return redirect('editform', form_template_id=form_template_id)

@login_required
def edit_question(request, form_template_id, question_id):
    question = get_object_or_404(Question, id=question_id)
    form_template = get_object_or_404(FormTemplate, id=form_template_id)
    if form_template.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this form.")

    if request.method == 'POST':
        question.question = request.POST.get('question')
        question.save()
        return redirect('editform', form_template_id=form_template.id)

    return render(request, 'editform.html', {'form_template': form_template, 'question': question, 'editing': True})

@login_required
def save_question(request, form_template_id, question_id):
    question = get_object_or_404(Question, id=question_id)
    form_template = get_object_or_404(FormTemplate, id=form_template_id)
    if form_template.user != request.user:
        return HttpResponseForbidden("You don't have permission to save this form.")

    if request.method == 'POST':
        question.question = request.POST.get('question')
        question.save()
        return redirect('editform', form_template_id=form_template.id)

    return HttpResponseBadRequest("Invalid request method.")

@login_required
def create_form(request, template_id):
    template = get_object_or_404(FormTemplate, pk=template_id)
    user = request.user  # Assuming the user is authenticated

    # Create a new Form linked to the template and the user
    form = Form.objects.create(template=template, user=user)

    # Retrieve all the questions associated with the template
    questions = Question.objects.filter(template=template)

    # Create a FormResponse for each question
    for question in questions:
        FormResponse.objects.create(form=form, question=question)
    
    responses = FormResponse.objects.filter(form=form)
    # Redirect to the newly created form's page or render a success message
    # redirect to record form
    return render(request, 'record.html', {'form': form, 'responses': responses})

@login_required
def upload_audio(request, form_id):
    if request.method == 'POST':
        form_instance = get_object_or_404(Form, id=form_id)
        audio_chunk = request.FILES.get('audioChunk')  # Get the uploaded audio file
        if audio_chunk:
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
            if request.POST.get('dataType') == 'mp4':
                converted_audio_bytes = audioconvert.mp4_to_webm(audio_bytes)
                transcribed_text = whisper.convert_audio(converted_audio_bytes, form_instance)
            else:
                transcribed_text = whisper.convert_audio(audio_bytes, form_instance)
            form_instance.transcript = transcribed_text
            form_instance.save()
        form_responses = form_instance.formresponse_set.all()
        for form_response in form_responses:
            gpt.process_form_query(form_response)
        
        return JsonResponse({'success': True})
        
    return JsonResponse({'success': False})

@login_required
def response_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    # have a setting to make form data public
    if form.user != request.user: # Only the forms attached to the user can be accessed
        return HttpResponseForbidden("You don't have permission to access this form.")

    form_responses = form.formresponse_set.all()

    return render(request, 'responseform.html', {'form': form, 'responses': form_responses})