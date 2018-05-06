# coding=utf-8
# Python imports
# Django imports
from django.db import models
from django.contrib.auth.models import User
# Third party app imports
# Local app imports
from history.models import LogUser, Activity
from post.models import Post
from discuss.models import Comment


class PostLike(models.Model):
    post = models.ForeignKey('post.Post', null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def add_log(self, estado):
        log = LogUser()
        log.activity = Activity.objects.get(activity="post_like")
        log.user = self.user
        if estado:
            log.description = u"Le gusta el post <a href='" + self.post.get_absolute_url() + "'>" + self.post.title + "</a>"
        else:
            log.description = u"Ha dejado de gustarle el post <a href='" + self.post.get_absolute_url() + "'>" + self.post.title + "</a>"
        log.pre_save()

    def __str__(self):
        return self.post.title + " " + self.user.username


class CommentLike(models.Model):
    comment = models.ForeignKey('discuss.Comment', null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def add_log(self, estado):
        log = LogUser()
        log.activity = Activity.objects.get(activity="comment_post_like")
        log.user = self.user
        if estado:
            log.description = "Le gusta el comentario <a href='" + self.comment.get_absolute_url() + "'>"
        else:
            log.description = "Ha dejado de gustarle el comentario <a href='" + self.comment.get_absolute_url() + "'>"
        log.pre_save()

    def __str__(self):
        return self.comment.content + " " + self.user.username