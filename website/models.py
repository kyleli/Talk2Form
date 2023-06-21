from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.core.validators import MaxValueValidator, MinValueValidator

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
    transcript = models.TextField(default="")

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
    response = models.TextField(default="Null")
    def truncated_response(self):
        if len(self.response) > 50:
            return self.response[:50] + "..."
        return self.response
    
    def __str__(self):
        return f"FormResponse ID: {self.id} | User: {self.question.template.user.username} | Form: {self.question.template.title} #{self.form.form_template_id} | Question: {self.question.question} | Response: {self.truncated_response()}"

class FormConfig(models.Model):
    AUDIO_RECOGNITION_MODEL_CHOICES = [
        ('whisper-1', 'whisper')
    ]
    AI_MODEL_CHOICES = [
        ('gpt-3.5-turbo', 'GPT-3.5'),
        ('gpt-3.5-turbo-16k', 'GPT-3.5-16k'),
        ('gpt-3.5-turbo-16k', 'GPT4'),
    ]
    form_template = models.OneToOneField('FormTemplate', on_delete=models.CASCADE)
    language = models.CharField(max_length=255, default = 'english')
    conversation_type = models.CharField(max_length=255, default='')
    audio_recognition_model_id = models.CharField(max_length=255, choices=AUDIO_RECOGNITION_MODEL_CHOICES, default='whisper-1')
    system_prompt = models.TextField(default='')
    ai_model_id = models.CharField(max_length=255, choices=AI_MODEL_CHOICES, default='gpt-3.5-turbo')
    temperature = models.DecimalField(max_digits=3, decimal_places=1, default=0.2, validators=[MaxValueValidator(2), MinValueValidator(-2)])
    presence_penalty = models.DecimalField(max_digits=3, decimal_places=1, default=-0.2, validators=[MaxValueValidator(2), MinValueValidator(-2)])

    def __str__(self):
        return f"Settings for FormTemplate ID: {self.form_template.id}"