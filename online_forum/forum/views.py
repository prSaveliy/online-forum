from django.shortcuts import render

from .models import Post

def post_feed(request):
    posts = Post.objects.all()
    return render(
        request,
        'forum/post/post_feed.html',
        {
            'posts': posts
        }
    )