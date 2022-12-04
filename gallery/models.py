    # coding=utf-8
# Python imports
# Django imports
from django.db import models
# Third party app imports
# Local app imports
from post.models import Post


def upload_location_postimage(instance, filename):
    return 'post/' + instance.post_slug + '/' + filename

# Create your models here.
class Image(models.Model):
    caption = models.CharField(null=False, blank=True, max_length=50, default="No caption")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    post_slug = models.SlugField(max_length=120)
    show_gallery = models.BooleanField(null=False, blank=False, default=False)
    image = models.ImageField(
        upload_to=upload_location_postimage,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.caption
