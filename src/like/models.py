# Python imports
# Django imports
from django.db import models
from django.contrib.auth.models import User
# Third party app imports
# Local app imports


class PostLike(models.Model):
    post = models.ForeignKey('post.Post', null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.post.title + " " + self.user.username


class CommentLike(models.Model):
    comment = models.ForeignKey('discuss.Comment', null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.comment.content + " " + self.user.username
