# Python imports
# Django imports
from django.db import models
# Third party app imports
# Local app imports


def upload_location_postimage(instance, filename):
    return 'post/%s/' % filename


# Create your models here.
class Image(models.Model):
    caption = models.CharField(null=False, blank=True, max_length=50, default="No caption")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    image = models.ImageField(
        upload_to=upload_location_postimage,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.caption
