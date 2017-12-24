# Python imports
# Django imports
from django.db import models
from django.core.urlresolvers import reverse
# Third party app imports
# Local app imports


# Create your models here.
# MVC Model View Controller
def upload_location_post(instance, filename):
    return 'posts/%s/%s' % (instance.profile.user.first_name, filename)


class Post(models.Model):
    STATUSES = (('IN', 'Inactive'), ('DR', 'Draft'), ('PB', 'Published'),)

    title = models.CharField(null=False, blank=False, max_length=120, default='none')
    content = models.TextField(null=False, blank=False, default='none')
    author = models.ForeignKey('user.UserProfile', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=2, choices=STATUSES, default='DR')
    num_likes = models.PositiveIntegerField(null=False, blank=False, default=0)
    published_date = models.DateTimeField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=upload_location_post,
        height_field='height_field',
        width_field='width_field'
    )

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'id': self.id})

    class Meta:
        ordering = ['-timestamp', '-updated']


class PostImage(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    image = models.ForeignKey('gallery.Image', on_delete=models.CASCADE)


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.post.title + ":" + self.category.id

    def __str__(self):
        return self.post.title + ":" + self.category.id


class PostComment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.ForeignKey('discuss.Comment', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-post', '-comment__timestamp']