# Python imports
# Django imports
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# Third party app imports
# Local app imports


# Common methods
def upload_location_author(instance, filename):
    return 'profiles/%s/%s' % (instance.user, filename)


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    location = models.CharField(max_length=30, blank=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to=upload_location_author,
        null=True,
        blank=True,
        height_field='height_field',
        width_field='width_field')
    image_url = models.URLField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if instance.social_auth:
            instance.userprofile.image_url = "https://twitter.com/" +\
                                             instance.social_auth.instance.username +\
                                             "/profile_image?size=original"
        instance.userprofile.save()

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    
    def get_absolute_url(self):
        return reverse('user:profile', kwargs={'user': self.user.username})

