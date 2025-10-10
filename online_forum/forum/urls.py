from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.post_feed, name='post_feed'),
    path('tag/<slug:tag_slug>/', views.post_feed, name='post_feed_by_slug'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>', views.post_detail, name='post_detail'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('<int:post_id>/', views.share_post, name='share_post')
]