# coding=utf-8
# Python imports
# Django imports
from django.contrib import admin
# Third party app imports
# Local app imports
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "content", "num_likes", "timestamp"]
    list_display_links = ["id"]
    list_editable = ["content", "num_likes"]
    list_filter = ["user"]
    search_fields = ["user"]

    class Meta:
        model = Comment


admin.site.register(Comment, CommentAdmin)
