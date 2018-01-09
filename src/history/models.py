# coding=utf-8
# Python imports
# Django imports
from django.contrib.auth.models import User
from django.db import models
# Third party app imports
# Local app imports


class Activity(models.Model):
    activity = models.CharField(primary_key=True, null=False, blank=False, max_length=20)
    icon = models.CharField(null=False, blank=False, max_length=20)

    def __str__(self):
        return self.activity


class LogUser(models.Model):
    PERMISSONS = (('*', 'Todos'), ('+', 'Friends'), ('-', 'Only me'),)

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    visibility = models.CharField(max_length=1, choices=PERMISSONS, default='-')

    def __str__(self):
        return self.user.username + ": " + self.activity.activity + " - " + self.description
