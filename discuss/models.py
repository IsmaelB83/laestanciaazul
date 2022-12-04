# coding=utf-8
# Python imports
# Django imports
from django.db import models
from django.contrib.auth.models import User
# Third party app imports
# Local app imports


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    num_likes = models.PositiveIntegerField(null=False, blank=False, default=0)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.content


