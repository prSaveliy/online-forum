from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User

from taggit.managers import TaggableManager


class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        default=1
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        unique_for_date='created',
        blank=True
    )
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="forum_posts"
    )
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(
            fields=['-created']
        )]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'forum:post_detail',
            args=[
                self.created.year,
                self.created.month,
                self.created.day,
                self.slug
            ]
        )
    
class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        default=1
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(
        default="",
        max_length=500,
    )
    
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(
            fields=['-created']
        )]

    def __str__(self):
        return f'Comment by {self.name}'
    
class Share(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="share"
    )

class LikePost(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes"
    )

class LikeComment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_likes"
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="comment_likes"
    )

    class Meta:
        unique_together = ('comment', 'user')
