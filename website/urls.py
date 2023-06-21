from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('usersettings', views.usersettings, name='usersettings'),
    path('editform/<int:form_template_id>/', views.editform, name='editform'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('create_default_form_template/', views.create_default_form_template, name='create_default_form_template'),
    path('form_template/<int:form_template_id>/delete/', views.delete_form_template, name='delete_form_template'),
    path('logout', views.logout, name='logout'),
    path('editform/<int:form_template_id>/edit_title/', views.edit_template_title, name='edit_template_title'),
    path('editform/<int:form_template_id>/save_title/', views.save_template_title, name='save_template_title'),
    path('create_question/<int:form_template_id>/', views.create_question, name='create_question'),
    path('editform/<int:form_template_id>/edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete_question/<int:form_template_id>/edit_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('editform/<int:form_template_id>/save_question/<int:question_id>/', views.save_question, name='save_question'),
    path('form_template/<int:form_template_id>/save_config/', views.save_form_config, name='save_form_config'),
    path('create_form/<int:template_id>/', views.create_form, name='create_form'),
    path('upload_audio/<int:form_id>/', views.upload_audio, name='upload_audio'),
    path('stop_audio/<int:form_id>/', views.stop_audio, name='stop_audio'),
    path('response_form/<int:form_id>/', views.response_form, name='response_form'),
    path('delete_account/', views.delete_account, name='delete_account')
]