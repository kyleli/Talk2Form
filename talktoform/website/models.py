from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    approval = models.BooleanField(default=False)

class FormTemplate(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Form(models.Model):
    template = models.ForeignKey(FormTemplate, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    template = models.ForeignKey(FormTemplate, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    editing = models.BooleanField(default=False)

class FormResponse(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField()


class AudioFile(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='audio_files/', default=None)