# coding=utf-8
# Python imports
# Django imports
from django.db import models
from django.core.urlresolvers import reverse
# Third party app imports
# Local app imports
from history.models import LogUser, Activity


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    sort = models.IntegerField(null=False, blank=False)
    name = models.CharField(null=False, blank=False, max_length=20)
    css_class = models.CharField(null=False, blank=False, max_length=20)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'id': self.id})

    def __iter__(self):
        return [self.id, self.sort, self.name, self.css_class, self.timestamp, self.updated]

    def add_log(self, user, operation):
        log = LogUser()
        if operation == "view":
            log.user = user
            log.activity = Activity.objects.get(activity="category_visit")
            log.description = u"Ha visitado la categoría de posts <a href='" + self.get_absolute_url() + "'>" + self.name + "</a>"
        log.pre_save()
        
    class Meta:
        ordering = ['sort']
