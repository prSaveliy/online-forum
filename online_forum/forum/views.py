from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.utils.text import slugify
from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
    SearchRank
)

from taggit.models import Tag

from .models import Post, Share, LikePost, LikeComment, Comment, User
from .forms import CommentForm, SharePostForm, PostCreationForm


def post_feed(request, tag_slug=None):
    tag = None
    posts = None

    if tag_slug:
        tag = get_object_or_404(
            Tag,
            slug=tag_slug
        )
        post_list = Post.objects.filter(tags__in=[tag])
    else:
        post_list = Post.objects.all()
    
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

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

    form = CommentForm()

    comment_list = post.comments.annotate(
        num_likes=Count('comment_likes')
    ).order_by('-num_likes', '-created')

    paginator = Paginator(comment_list, 10)
    page_number = request.GET.get('page', 1)

    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    # handle number of shares
    shares_gt_99 = False
    if post.share.count() > 99:
        shares_gt_99 = True

    # handle number of comments
    comms_gt_99 = False
    if post.comments.count() > 99:
        comms_gt_99 = True

    # handle post like icon change
    liked = False
    if request.user.is_authenticated:
        if post.likes.filter(post=post, user=request.user).exists():
            liked = True
        else:
            liked = False

    return render(
        request,
        'forum/post/post_detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'shares_gt_99': shares_gt_99,
            'comms_gt_99': comms_gt_99,
            'liked': liked,
            'comment_list': comment_list
        }
    )

@require_POST
def post_comment(request, post_id):
    if not request.user.is_authenticated:
        return redirect("users:login")
    
    post = get_object_or_404(
        Post,
        id=post_id
    )

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()

    return redirect(
        'forum:post_detail',
        year=post.created.year,
        month=post.created.month,
        day=post.created.day,
        slug=post.slug
    )

def share_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("users:login")
    
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
                f'{request.user.username} ({cd['email']}) recommends you check out "{post.title}" on Forum'
            )
            message = (
                f'Read and comment "{post.title}" on {post_url}\n\n'
                f"{request.user.username}'s comment:\n {cd['comment']}"
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
        
    else:
        form = SharePostForm()

    return render(
        request,
        'forum/post/share_post.html',
        {
            'post': post,
            'sent': sent,
            'form': form
        }

    )

def handle_likes(request, post_id):
    if not request.user.is_authenticated:
        return redirect("users:login")

    post = get_object_or_404(
        Post,
        id=post_id
    )

    like, created = LikePost.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()

    return redirect(
        'forum:post_detail',
        year=post.created.year,
        month=post.created.month,
        day=post.created.day,
        slug=post.slug
    )

def handle_comment_likes(request, post_id, comment_id):
    if not request.user.is_authenticated:
        return redirect("users:login")

    post = get_object_or_404(
        Post,
        id=post_id
    )
    comment = get_object_or_404(
        Comment,
        post=post,
        id=comment_id
    )

    like, created = LikeComment.objects.get_or_create(comment=comment, user=request.user)

    if not created:
        like.delete()

    page_number = request.GET.get('page', 1)
    year=post.created.year
    month=post.created.month
    day=post.created.day
    slug=post.slug
    
    if page_number == '1':
        return redirect(
            f'/{year}/{month}/{day}/{slug}'
        )
    else:
        return redirect(
            f'/{year}/{month}/{day}/{slug}?page={page_number}'
        )

def handle_likes_home_page(request, post_id):
    if not request.user.is_authenticated:
        return redirect("users:login")

    post = get_object_or_404(
        Post,
        id=post_id
    )

    like, created = LikePost.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()

    page_number = request.GET.get('page', 1)

    return redirect(
        f"/?page={page_number}"
    )

def profile_page(request, user_id):
    user = get_object_or_404(
        User,
        id=user_id
    )
    post_list = user.posts.filter(user=user)
    total_likes = 0
    for post in post_list:
        total_likes += post.likes.count()

    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'forum/profile/profile_page.html',
        {
            'total_likes': total_likes,
            'posts': posts,
            'user': user
        }
    )

def handle_likes_profile(request, post_id):
    if not request.user.is_authenticated:
        return redirect("users:login")

    post = get_object_or_404(
        Post,
        id=post_id
    )

    like, created = LikePost.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()

    page_number = request.GET.get('page', 1)

    return redirect(
        f"/profile/{request.user.id}/?page={page_number}"
    )

def title_slugify(title):
    slug = slugify(title)
    unique_slug = slug
    counter = 1

    while Post.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{slug}-{counter}'
        counter += 1
    return unique_slug

def create_post(request):
    if not request.user.is_authenticated:
        return redirect("users:login")
    
    if request.method == "POST":
        form = PostCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = title_slugify(form.cleaned_data['title'])
            post.user = request.user
            post.author = request.user
            post.save()
            form.save_m2m()

            return redirect("forum:profile_page", request.user.id)
    else:
        form = PostCreationForm()

    return render(
        request,
        'forum/post/create_post.html',
        {
            'form': form
        }
    )

def delete_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(
            Post,
            id=post_id
        )
        if request.user == post.user:
            post.delete()

    return redirect("forum:profile_page", post.user.id)

def delete_comment(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(
            Comment,
            id=comment_id
        )
        post = comment.post
        if request.user == comment.user:
            comment.delete()

    return redirect(
        "forum:post_detail",
        year=post.created.year,
        month=post.created.month,
        day=post.created.day,
        slug=post.slug
    )

def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        search_vector = SearchVector('title', 'content')
        search_query = SearchQuery(query)
        results = Post.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('-rank')

    paginator = Paginator(results, 5)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'forum/post/search.html',
        {
            'posts': posts,
            'query': query
        }
    )

def handle_likes_search(request, post_id):
    if not request.user.is_authenticated:
        return redirect("users:login")

    post = get_object_or_404(
        Post,
        id=post_id
    )

    like, created = LikePost.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()

    query = request.GET.get('q')
    page_number = request.GET.get('page', 1)

    return redirect(
        f"/search/?q={query}&page={page_number}"
    )