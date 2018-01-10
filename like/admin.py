# coding=utf-8
# Python imports
# Django imports
from django.db import models
from django.contrib import admin
# Third party app imports
# Local app imports
from .models import PostLike, CommentLike


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "user", "ip", "timestamp"]
    list_display_links = ["id", "post"]
    list_editable = [   "user", "ip"]
    list_filter = ["post", "user"]
    search_fields = ["post", "user"]

    class Meta:
        model = PostLike


class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ["id", "comment", "user", "ip", "timestamp"]
    list_display_links = ["id"]
    list_editable = ["comment", "user", "ip"]
    list_filter = ["comment", "user"]
    search_fields = ["comment", "user"]

    class Meta:
        model = CommentLike


admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
