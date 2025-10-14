from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('logging_out/', views.logging_out, name='logging_out'),
    path('register/', views.register, name='register')
]