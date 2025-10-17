from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.post_feed, name='post_feed'),
    path('tag/<slug:tag_slug>/', views.post_feed, name='post_feed_by_slug'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>', views.post_detail, name='post_detail'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('<int:post_id>/', views.share_post, name='share_post'),
    path('<int:post_id>/like/', views.handle_likes, name='handle_likes'),
    path('<int:post_id>/<int:comment_id>/like_comment/', views.handle_comment_likes, name='handle_comment_likes'),
    path('home/<int:post_id>/like/', views.handle_likes_home_page, name='handle_likes_home_page'),
]