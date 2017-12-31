# Python imports
# Django imports
from django.contrib import admin
# Third party app imports
# Local app imports
from .models import Activity, LogUser


class ActivityAdmin(admin.ModelAdmin):
    list_display = ["activity", "icon"]
    list_display_links = ["activity"]
    list_editable = ["icon"]
    list_filter = ["activity"]
    search_fields = ["activity"]

    class Meta:
        model = Activity


class LogUserAdmin(admin.ModelAdmin):
    list_display = ["id", "activity", "user", "description", "timestamp", "visibility"]
    list_display_links = ["id"]
    list_editable = ["activity", "user", "description", "visibility"]
    list_filter = ["activity", "user"]
    search_fields = ["activity", "user"]

    class Meta:
        model = LogUser


admin.site.register(Activity, ActivityAdmin)
admin.site.register(LogUser, LogUserAdmin)