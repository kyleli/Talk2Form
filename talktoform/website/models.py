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
    def __str__(self):
        return f"User ID: {self.id} | User: {self.username}"

class FormTemplate(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FormTemplate ID: {self.id} | User: {self.user.username} | Template: {self.title}"


class Form(models.Model):
    template = models.ForeignKey(FormTemplate, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    form_template_id = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.pk is None:  # New form instance
            # Retrieve the count of forms based on the associated FormTemplate
            form_count = Form.objects.filter(template=self.template).count()
            # Increment the count and assign it to form_template_id
            self.form_template_id = form_count + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Form ID: {self.id} | User: {self.user.username} | Form: {self.template.title} #{self.form_template_id}"


class Question(models.Model):
    template = models.ForeignKey(FormTemplate, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    editing = models.BooleanField(default=False)
    def __str__(self):
        return f"Question ID: {self.id} | User: {self.template.user.username} | Template: {self.template.title} | Question: {self.question}"

class FormResponse(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField(default="Processing...")

    def truncated_response(self):
        if len(self.response) > 50:
            return self.response[:50] + "..."
        return self.response
    
    def __str__(self):
        return f"FormResponse ID: {self.id} | User: {self.question.template.user.username} | Form: {self.question.template.title} #{self.form.form_template_id} | Question: {self.question.question} | Response: {self.truncated_response()}"


class AudioFile(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    audio_file = models.FileField(storage=default_storage, upload_to='audio_files/', default=None)
    def __str__(self):
        return f"AudioFile ID: {self.id} | User: {self.form.template.user.username} | Form: {self.form.template.title} #{self.form.form_template_id} | Audio: {self.audio_file}"

# If you run into Windows Fatal Exception: Access Violations when running 'python mnaage.py test', this is the reason it's trying to delete stuff the test doesn't have access to
@receiver(post_delete, sender=AudioFile)
def delete_audio_file(sender, instance, **kwargs):
    # Delete the file from the storage
    instance.audio_file.delete(save=False)