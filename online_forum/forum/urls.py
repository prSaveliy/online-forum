from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.post_feed, name='post_feed'),
]