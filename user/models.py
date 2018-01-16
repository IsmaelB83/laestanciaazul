# coding=utf-8
# Python imports
# Django imports
from django.core.files import File
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# Third party app imports
# Local app imports
from history.models import LogUser, Activity


def upload_location_author(instance, filename):
    return 'profiles/%s/%s' % (instance.user, filename)


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    country = models.CharField(max_length=20, blank=True, null=False)
    location = models.CharField(max_length=30, blank=True, null=False)
    description = models.CharField(max_length=100, blank=True, null=False)
    introduction = models.TextField(blank=True, null=False)
    image = models.ImageField(
        upload_to=upload_location_author,
        null=False,
        blank=False)
    author = models.BooleanField(null=False, blank=False, default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if instance.social_auth and not instance.userprofile.image:
            # r = requests.get(staticfiles_storage.url('img/user_social.gif'))
            # with open('/tmp/user_social.gif', 'wb') as f:
            #     f.write(r.content)
            # reopen = open('/tmp/user_social.gif', 'rb')
            # django_file = File(reopen)
            # instance.userprofile.image.save('user_social.gif', django_file, save=True)
            reopen = open('/home/trama/static_cdn/img/user_social.gif', 'rb')
            django_file = File(reopen)
            instance.userprofile.image.save('user_social.gif', django_file, save=True)
        instance.userprofile.save()

    def add_log(self, visited_user, operation):
        if self.user != visited_user.user:
            log = LogUser()
            if operation == "edit":
                log.user = self.user
                log.activity = Activity.objects.get(activity="user_edit")
                log.description = "Ha editado el usuario <a href='" + self.get_absolute_url() + "'>" + self.user.first_name + " " + self.user.last_name + "</a>"
            if operation == "view":
                log.user = self.user
                log.activity = Activity.objects.get(activity="user_visit")
                log.description = "Ha visitado el perfil del usuario <a href='" + visited_user.get_absolute_url() + "'>" + visited_user.user.first_name + " " + visited_user.user.last_name + "</a>"
            log.pre_save()
        
    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    
    def get_absolute_url(self):
        return reverse('user:profile', kwargs={'id': self.user.id})


# Create your models here.
class UserFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')

    class Meta:
        unique_together = (('user', 'follows'),)

    def __unicode__(self):
        return self.user.username + " " + self.follow_user.username

    def __str__(self):
        return self.user.username + " " + self.follow_user.username
