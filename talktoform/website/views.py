from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def usersettings(request):
    return render(request, 'usersettings.html')

def form(request):
    return render(request, 'form.html')

def dashboard(request):
    return render(request, 'dashboard.html')