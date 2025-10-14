from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.mail import send_mail

from taggit.models import Tag

from .models import Post, Share, Like
from .forms import CommentForm, SharePostForm


def post_feed(request, tag_slug=None):
    tag = None
    posts = None

    if tag_slug:
        tag = get_object_or_404(
            Tag,
            slug=tag_slug
        )
        posts = Post.objects.filter(tags__in=[tag])
    else:
        posts = Post.objects.all()

    return render(
        request,
        'forum/post/post_feed.html',
        {
            'posts': posts,
            'tag': tag
        }
    )

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        created__year=year,
        created__month=month,
        created__day=day,
        slug=slug
    )

    comments = post.comments.all()
    form = CommentForm()
    pressed = False

    return render(
        request,
        'forum/post/post_detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'pressed': pressed
        }
    )

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id
    )

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return redirect(
        'forum:post_detail',
        year=post.created.year,
        month=post.created.month,
        day=post.created.day,
        slug=post.slug
    )

def share_post(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id
    )

    sent = False

    if request.method == 'POST':
        form = SharePostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f'{cd['name']} recommends you check out "{post.title}" on Forum'
            )
            message = (
                f'Read and comment "{post.title}" on {post_url}\n\n'
                f"{cd['name']}'s comment:\n {cd['comment']}"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[
                    cd['to']
                ]
            )
            sent = True
            Share.objects.create(post=post)

    # handle number of shares
    shares_gt_99 = False
    if post.share.count() > 99:
        shares_gt_99 = True

    # handle number of comments
    comms_gt_99 = False
    if post.comments.count() > 99:
        comms_gt_99 = True
            
    else:
        form = SharePostForm()

    return render(
        request,
        'forum/post/share_post.html',
        {
            'post': post,
            'sent': sent,
            'form': form,
            'shares_gt_99': shares_gt_99,
            'comms_gt_99': comms_gt_99
        }

    )

def handle_like_pressed(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        created__year=year,
        created__month=month,
        created__day=day,
        slug=slug
    )

    Like.objects.create(post=post)
    pressed = True
    comments = post.comments.all()
    form = CommentForm()

    return render(
        request,
        'forum/post/post_detail.html',
        {
            'pressed': pressed,
            'post': post,
            'comments': comments,
            'form': form
        }
    )

def handle_like_unpressed(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        created__year=year,
        created__month=month,
        created__day=day,
        slug=slug
    )

    num_likes = post.likes.count()
    Like.objects.get(id=num_likes).delete()
    pressed = False
    comments = post.comments.all()
    form = CommentForm()

    return render(
        request,
        'forum/post/post_detail.html',
        {
            'pressed': pressed,
            'post': post,
            'comments': comments,
            'form': form
        }
    )

# add User model
