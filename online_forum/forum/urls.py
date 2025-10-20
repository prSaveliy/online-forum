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
    path('profile/<int:user_id>/', views.profile_page, name='profile_page'),
    path('profile/<int:post_id>/like', views.handle_likes_profile, name='handle_likes_profile'),
    path('create_post/', views.create_post, name='create_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('search/', views.search, name='search'),
    path('search/<int:post_id>/like', views.handle_likes_search, name='handle_likes_search')
]