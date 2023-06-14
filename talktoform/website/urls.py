from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('usersettings', views.usersettings, name='usersettings'),
    path('form', views.form, name='form'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('create_default_form_template/', views.create_default_form_template, name='create_default_form_template'),
    path('logout', views.logout, name='logout'),
]