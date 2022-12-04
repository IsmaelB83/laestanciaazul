# coding=utf-8
# Python imports
# Django imports
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Third party app imports

class Post(models.Model):
    STATUSES = (('IN', 'Inactive'), ('DR', 'Draft'), ('PB', 'Published'),)

    id = models.SlugField(primary_key=True, max_length=120)
    title = models.CharField(null=False, blank=False, max_length=120, default='none')
    summary = models.TextField(null=False, blank=False, default='none', max_length=300)
    content = models.TextField(null=False, blank=False, default='none')
    author = models.ForeignKey('user.UserProfile', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=2, choices=STATUSES, default='DR')
    published_date = models.DateTimeField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    image = models.ForeignKey('gallery.Image', null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'id': self.id})

    class Meta:
        ordering = ['-timestamp', '-updated']


class PostImage(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    image = models.ForeignKey('gallery.Image', on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title + ": " + self.post.image.caption


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title + ": " + self.category.id


class PostComment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.ForeignKey('discuss.Comment', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-post', '-comment__timestamp']

    def __str__(self):
        return self.post.title + ": " + self.comment.content


class PostArchive(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    posts = models.PositiveIntegerField()

    class Meta:
        unique_together = (('year', 'month'),)
        ordering = ['-year']


class PostView(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    ip = models.GenericIPAddressField(null=False, blank=False)

    class Meta:
        ordering = ['-date']


class PostLike(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        unique_together = (('post', 'user'),)
        ordering = ['-date']