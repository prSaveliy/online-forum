from django import template
from datetime import datetime
from django.db.models import Count

from taggit.models import Tag

from forum.models import Post


register = template.Library()

@register.filter(name='error_char')
def count_error_char(errors):
    """handling errors in the registration template"""
    ls = list(errors)
    if not len(ls):
        return None
    return len(ls[0]) > 50

@register.filter(name='timepassed')
def count_time_passed(model):
    """counts the time passed from model creation"""
    created = model.created
    time_now = datetime.now(created.tzinfo)
    time_difference = time_now - created

    total_seconds = int(time_difference.total_seconds())

    minutes = total_seconds // 60
    hours = minutes // 60
    days = hours // 24
    months = days // 30
    years = months // 12

    if not minutes:
        return f'{total_seconds}s ago'
    if not hours:
        return f'{minutes}m ago'
    if not days:
        return f'{hours}h ago'
    if not months:
        return f'{days}d ago'
    if not years:
        return f'{months}mon ago'
    return f'{years}y ago'

@register.filter(name='like_exists')
def check_like_exists_comment(comment, request_user):
    if request_user.is_authenticated:
        if comment.comment_likes.filter(comment=comment, user=request_user).exists():
            return True
        return False

@register.filter(name='post_like_exists')
def check_like_exists_post(post, request_user):
    if request_user.is_authenticated:
        if post.likes.filter(user=request_user).exists():
            return True
        return False
    
@register.simple_tag
def get_most_popular_tags(max=3):
    return Tag.objects.annotate(
        posts=Count('taggit_taggeditem_items')
    ).order_by('-posts')[:max]

@register.filter(name='count_posts_tagged')
def count_posts_tagged_by_tag(tag):
    return tag.posts

@register.simple_tag
def get_most_liked_posts(max=3):
    return Post.objects.annotate(
        num_likes=Count('likes')
    ).order_by('-num_likes')[:max]

@register.filter(name='count_likes_post')
def count_likes_on_post(post):
    return post.likes.count()
    
@register.simple_tag
def get_most_commented_posts(max=3):
    return Post.objects.annotate(
        num_comments=Count('comments')
    ).order_by('-num_comments')[:max]

@register.filter(name='count_comments_post')
def count_comments_on_post(post):
    return post.comments.count()