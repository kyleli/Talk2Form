from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import FormTemplate

# Create your views here.
def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Incorrect username or password.')
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
        confirmpassword = request.POST.get('confirmpassword')

        try:
            validate_email(email)  # Check if the email is valid
        except ValidationError:
            messages.info(request, 'Invalid Email Address')
            return redirect('signup')

        if password == confirmpassword:
            try:
                validate_password(password)  # Check password strength
            except ValidationError as e:
                messages.info(request, ', '.join(e.messages))
                return redirect('signup')

            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Registered')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=email, email=email, password=password)
                user.save()
                return redirect('index')
        else:
            messages.info(request, 'Passwords Do Not Match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

@login_required
def usersettings(request):
    return render(request, 'usersettings.html')

@login_required
def form(request):
    return render(request, 'form.html')

@login_required
def dashboard(request):
    user = request.user
    form_templates = FormTemplate.objects.filter(user=user)
    return render(request, 'dashboard.html', {'form_templates': form_templates})

@login_required
def create_default_form_template(request):
    if request.method == 'POST':
        title = 'New Form'
        body = 'Form description'
        user = request.user
        FormTemplate.objects.create(title=title, body=body, user=user)
        return redirect('dashboard')
    return render(request, 'dashboard.html')