from django.contrib import admin

# Register your models here.
from .models import Post

# More info here: https://docs.djangoproject.com/en/1.11/intro/tutorial07/
class PostModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
