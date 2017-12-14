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
    num_comments = models.PositiveIntegerField(null=False, blank=False)
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
        return reverse("blog:post", kwargs={"id": self.id})

    class Meta:
        ordering = ['-timestamp', '-updated']


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    sort = models.IntegerField(null=False, blank=False)
    category = models.CharField(null=False, blank=False, max_length=20)
    css_class = models.CharField(null=False, blank=False, max_length=20)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    thumbnail = models.ImageField(upload_to=upload_location, null=True, blank=True, height_field="height_field", width_field="width_field")

    def __unicode__(self):
        return self.category

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"id": self.id})

    class Meta:
        ordering = ['sort']


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        unique_together = (("post", "category"),)
        ordering = ['-post', 'category']


class PostComment(models.Model):
    num_comment = models.PositiveIntegerField(null=False, blank=False)
    user = models.CharField(null=False, blank=False, max_length=20)
    comment = models.TextField(null=False, blank=False)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    num_likes = models.PositiveIntegerField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        unique_together = (("post", "num_comment"),)
        ordering = ['post', '-num_comment']
