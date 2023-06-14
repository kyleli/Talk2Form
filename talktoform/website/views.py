from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

from django.contrib.auth.password_validation import validate_password

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

def usersettings(request):
    return render(request, 'usersettings.html')

def form(request):
    return render(request, 'form.html')

def dashboard(request):
    return render(request, 'dashboard.html')