from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('usersettings', views.usersettings, name='usersettings'),
    path('editform/<int:form_template_id>/', views.editform, name='editform'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('create_default_form_template/', views.create_default_form_template, name='create_default_form_template'),
    path('logout', views.logout, name='logout'),
    path('editform/<int:form_template_id>/edit_title/', views.edit_template_title, name='edit_template_title'),
    path('editform/<int:form_template_id>/save_title/', views.save_template_title, name='save_template_title'),
    path('create_question/<int:form_template_id>/', views.create_question, name='create_question'),
    path('editform/<int:form_template_id>/edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('editform/<int:form_template_id>/save_question/<int:question_id>/', views.save_question, name='save_question'),
    path('create_form/<int:template_id>/', views.create_form, name='create_form'),
    path('record/<int:form_id>/', views.record_form, name='record'),

]