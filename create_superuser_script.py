import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    username = 'admin'  # Set your desired username
    email = 'admin@example.com'  # Set your desired email
    password = 'password'  # Set your desired password

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print('Superuser created successfully.')
    else:
        print('Superuser already exists.')

create_superuser()
