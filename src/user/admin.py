# Python imports
# Django imports
from django.contrib import admin
# Third party app imports
# Local app imports
from .models import UserProfile


# Register your models here.
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "location", "birth_date", "image"]
    list_display_links = ["id", "user"]
    list_editable = ["location", "birth_date"]
    list_filter = ["user"]
    search_fields = ["user"]
    
    class Meta:
        model = UserProfile


admin.site.register(UserProfile, ProfileModelAdmin)
