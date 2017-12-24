# Python imports
# Django imports
from django.contrib import admin
# Third party app imports
# Local app imports
from .models import Image


# Register your models here.
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ["id", "caption", "image", "timestamp"]
    list_display_links = ["id"]
    list_editable = ["caption", "image"]
    list_filter = ["caption"]
    search_fields = ["caption"]

    class Meta:
        model = Image
