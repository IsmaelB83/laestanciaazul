# Python imports
# Django imports
from django.contrib import admin
# Third party app imports
# Local app imports
from .models import UserProfile


# Register your models here.
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ["user", "location", "image"]
    list_display_links = ["user"]
    list_editable = ["location"]
    list_filter = ["user"]
    search_fields = ["user"]
    
    class Meta:
        model = UserProfile


admin.site.register(UserProfile, ProfileModelAdmin)
