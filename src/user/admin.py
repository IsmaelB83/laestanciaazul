# coding=utf-8
# Python imports
# Django imports
from django.contrib import admin
# Third party app imports
# Local app imports
from .models import UserProfile, UserFollow


# Register your models here.
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ["user", "country", "location", "description", "image"]
    list_display_links = ["user"]
    list_editable = ["country", "location", "description"]
    list_filter = ["user"]
    search_fields = ["user"]
    
    class Meta:
        model = UserProfile


class UserFollowAdmin(admin.ModelAdmin):
    list_display = ["user", "follows"]
    list_display_links = ["user"]
    list_editable = ["follows"]
    list_filter = ["user"]
    search_fields = ["user"]

    class Meta:
        model = UserFollow


admin.site.register(UserProfile, ProfileModelAdmin)
admin.site.register(UserFollow, UserFollowAdmin)
