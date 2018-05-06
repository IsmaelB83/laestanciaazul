    # coding=utf-8
# Python imports
# Django imports
from django.db import models
# Third party app imports
# Local app imports
from history.models import LogUser, Activity
from post.models import Post


def upload_location_postimage(instance, filename):
    return 'post/' + instance.post_slug + '/' + filename


def add_log(user):
    log = LogUser()
    log.user = user
    log.activity = Activity.objects.get(activity="gallery_visit")
    log.description = u"Ha visitado la galería de imagenes"
    log.pre_save()


# Create your models here.
class Image(models.Model):
    caption = models.CharField(null=False, blank=True, max_length=50, default="No caption")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    post_slug = models.SlugField(max_length = 120)
    image = models.ImageField(
        upload_to=upload_location_postimage,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.caption
