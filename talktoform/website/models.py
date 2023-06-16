from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

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
    audio_file = models.FileField(storage=default_storage, upload_to='audio_files/', default=None)

# If you run into Windows Fatal Exception: Access Violations when running 'python mnaage.py test', this is the reason it's trying to delete stuff the test doesn't have access to
@receiver(post_delete, sender=AudioFile)
def delete_audio_file(sender, instance, **kwargs):
    # Delete the file from the storage
    instance.audio_file.delete(save=False)