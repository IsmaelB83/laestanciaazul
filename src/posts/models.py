from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

# Create your models here.
# MVC Model View Controller
def upload_location_post(instance, filename):
    return '%s/%s' % (instance.author.user.first_name, filename)


def upload_location_author(instance, filename):
    return '%s/%s' % (instance.user, filename)


def upload_location_postimage(instance, filename):
    return '%s/%i/%s' % (instance.post.author.user.first_name, instance.post.id, filename)


class Post(models.Model):
    STATUSES = (('IN', 'Inactive'), ('DR', 'Draft'), ('PB', 'Published'),)

    title = models.CharField(null=False, blank=False, max_length=120, default='none')
    content = models.TextField(null=False, blank=False, default='none')
    author = models.ForeignKey('Author', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=2, choices=STATUSES, default='DR')
    num_likes = models.PositiveIntegerField(null=False, blank=False, default=0)
    published_date = models.DateTimeField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    image = models.ImageField(
        null=True, blank=True, upload_to=upload_location_post, height_field='height_field', width_field='width_field')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'id': self.id})

    class Meta:
        ordering = ['-timestamp', '-updated']


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    sort = models.IntegerField(null=False, blank=False)
    category = models.CharField(null=False, blank=False, max_length=20)
    css_class = models.CharField(null=False, blank=False, max_length=20)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.category

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'id': self.id})

    def __iter__(self):
        return [self.id, self.sort, self.category, self.css_class, self.timestamp, self.updated]

    class Meta:
        ordering = ['sort']


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        unique_together = (('post', 'category'),)
        ordering = ['-post', 'category']

    def __unicode__(self):
        return self.post.title + ":" + self.category.id

    def __str__(self):
        return self.post.title + ":" + self.category.id


class PostComment(models.Model):
    num_comment = models.PositiveIntegerField(null=False, blank=False)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, blank=True, null=True)
    anonymous_name = models.CharField(null=False, blank=True, default='none', max_length=30)
    anonymous_email = models.EmailField(null=False, blank=True, default='none@none.com', max_length=40)
    comment = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        unique_together = (('post', 'num_comment'),)
        ordering = ['post', '-num_comment']


class PostImage(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    caption = models.CharField(null=False, blank=True, max_length=50, default="No caption")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    image = models.ImageField(upload_to=upload_location_postimage, null=True, blank=True, height_field='height_field', width_field='width_field')


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    birth_date = models.DateField(null=True, blank=True)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    image = models.ImageField(upload_to=upload_location_author, null=True, blank=True, height_field='height_field', width_field='width_field')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Author.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if instance.is_superuser == False:
            instance.author.save()

    def __unicode__(self):
        return self.user.first_name

    def __str__(self):
        return self.user.first_name

    def get_absolute_url(self):
        return reverse('blog:profile', kwargs={'id': self.id})


class SocialProfile(models.Model):
    """Main SocialProfile Object - Holds extra profile data retrieved from auth providers"""
    GENDER_CHOICES = ((_('male'), _('Male')), (_('female'), _('Female')), (_('other'), _('Other')), ('', ''))

    user = models.OneToOneField(User, related_name='social_profile', verbose_name=_("Social Profile"))
    gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES, verbose_name=_("Gender"))
    url = models.URLField(blank=True, verbose_name=_("Homepage"), help_text=_("Where can we find out more about you?"), max_length=500)
    image_url = models.URLField(blank=True, verbose_name=_("Avatar Picture"), max_length=500)
    description = models.TextField(blank=True, verbose_name=_("Description"), help_text=_("Tell us about yourself!"))
    manually_edited = models.BooleanField(default=False)

    class Meta(object):
        verbose_name = _("Social Profile")
        verbose_name_plural = _("Social Profiles")
        ordering = ['user__username']

    def __str__(self):
        return self.user.username

    @models.permalink
    def get_absolute_url(self):
        return 'sp_profile_other_view_page', [self.user.username]


def create_user_profile(sender, instance, created, **kwargs):
    """Creates a UserProfile Object Whenever a User Object is Created"""
    if created:
        SocialProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
