from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
# MVC Model View Controller
def upload_location(instance, filename):
    return "%s/%i/%s" % (instance.author, instance.id, filename)


class Post(models.Model):
    title = models.CharField(null=False, blank=False, max_length=120)
    content = models.TextField(null=False, blank=False)
    author = models.CharField(null=False, max_length=20)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    caption = models.URLField()
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        height_field="height_field",
        width_field="width_field")

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-updated"]
