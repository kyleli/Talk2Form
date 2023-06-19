from django.contrib import admin
from .models import User, FormTemplate, Form, Question, FormResponse, FormConfig

# Register your models here.
admin.site.register(User)
admin.site.register(FormTemplate)
admin.site.register(Form)
admin.site.register(Question)
admin.site.register(FormResponse)
admin.site.register(FormConfig)