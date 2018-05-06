# coding=utf-8
# Python imports
from datetime import datetime
# Django imports
from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
# Third party app imports
# Local app imports
from history.models import LogUser, Activity


def add_log_search(user, search):
    log = LogUser()
    log.user = user
    log.activity = Activity.objects.get(activity="search")
    log.description = "Se ha realizado la siguiente búsqueda: " + search
    log.pre_save()


def add_log_archive(user, archive):
    log = LogUser()
    log.user = user
    log.activity = Activity.objects.get(activity="archive")
    log.description = "Se ha accedido al archivo: " + archive
    log.pre_save()


class Post(models.Model):
    STATUSES = (('IN', 'Inactive'), ('DR', 'Draft'), ('PB', 'Published'),)

    title = models.CharField(null=False, blank=False, max_length=120, default='none')
    content = models.TextField(null=False, blank=False, default='none')
    author = models.ForeignKey('user.UserProfile', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=2, choices=STATUSES, default='DR')
    published_date = models.DateTimeField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    image = models.ForeignKey('gallery.Image', null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(max_length = 120)

    def add_log(self, user, operation):
        log = LogUser()
        log.user = user
        if operation == "create":
            log.activity = Activity.objects.get(activity="post_create")
            log.description = u"Ha creado el post <a href='" + self.get_absolute_url() + "'>" + self.title + "</a>"
        elif operation == "edit":
            log.activity = Activity.objects.get(activity="post_edit")
            log.description = u"Ha editado el post <a href='" + self.get_absolute_url() + "'>" + self.title + "</a>"
        elif operation == "view":
            log.activity = Activity.objects.get(activity="post_visit")
            log.description = u"Ha visitado el post <a href='" + self.get_absolute_url() + "'>" + self.title + "</a>"
        log.pre_save()

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


class PostImageSmall(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    image = models.ForeignKey('gallery.Image', on_delete=models.CASCADE)
    
    def __str__(self):
        return ""
        #return self.post.title + ": " + self.post.image.caption


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

    def add_log(self, operation):
        log = LogUser()
        log.user = self.comment.user
        if operation == "create":
            log.activity = Activity.objects.get(activity="comment_post_create")
            log.description = "Ha creado el comentario <a href='" + self.post.get_absolute_url() + "#form_comments'>" + self.comment.content[:15] + "...</a>"
        log.pre_save()
        
    def __str__(self):
        return self.post.title + ": " + self.comment.content


class PostArchive(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    posts = models.PositiveIntegerField()

    class Meta:
        unique_together = (('year', 'month'),)
        ordering = ['-year']
