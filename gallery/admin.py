# coding=utf-8
# Python imports
# Django imports
from django.contrib import admin
# Third party app imports
# Local app imports
from .models import Image


# Register your models here.
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ["id", "caption", "image", "post_slug"]
    list_display_links = ["id"]
    list_editable = ["caption", "image", "post_slug"]
    list_filter = ["post_slug"]
    search_fields = ["caption"]

    class Meta:
        model = Image


admin.site.register(Image, ImageModelAdmin)
