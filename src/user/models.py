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
    return 'authors/%s/%s' % (instance.user, filename)


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    birth_date = models.DateField(null=True, blank=True)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to=upload_location_author,
        null=True,
        blank=True,
        height_field='height_field',
        width_field='width_field')
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Author.objects.create(user=instance)
            # socials = UserSocialAuth.objects.all()
            #  if socials:
            #     author = Author.objects.get(user=instance)
            #     author.location = "Social"
            #     author.description = socials[0].provider + " user"
            #     if socials[0].provider == "twitter":
            #         img_temp = NamedTemporaryFile(delete=True)
            #         img_temp.write(urlopen("https://twitter.com/" + socials[0] + "/profile_image?size=original").read())
            #         img_temp.flush()
            #         author.image.save(author+"_photo", File(img_temp), save=True)
            #         author.save()
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if not instance.is_superuser:
            instance.author.save()
    
    def __unicode__(self):
        return self.user.first_name
    
    def __str__(self):
        return self.user.first_name
    
    def get_absolute_url(self):
        return reverse('blog:profile', kwargs={'id': self.id})
