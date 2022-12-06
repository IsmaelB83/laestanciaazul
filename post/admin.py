# coding=utf-8
# Python imports
# Django imports
from django.contrib import admin
# Third party app imports
# Local app imports
from .models import Post, PostCategory, PostImage, PostComment, PostArchive, PostView, PostLike


# More info here: https://docs.djangoproject.com/en/1.11/intro/tutorial07/
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "published_date", "status", "image"]
    list_display_links = ["title"]
    list_editable = ["content", "status", "image"]
    list_filter = ["published_date"]
    search_fields = ["title", "content"]

    class Meta:
        model = Post


class PostCategoryModelAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "category"]
    list_display_links = ["id"]
    list_editable = ["post", "category"]
    list_filter = ["category"]

    class Meta:
        model = PostCategory


class PostImageModelAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "image"]
    list_display_links = ["id"]
    list_editable = ["post", "image"]
    list_filter = ["post"]

    class Meta:
        model = PostImage


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "comment"]
    list_display_links = ["id"]
    list_editable = ["post", "comment"]
    list_filter = ["post"]

    class Meta:
        model = PostComment


class PostArchiveAdmin(admin.ModelAdmin):
    list_display = ["id", "year", "month", "posts"]
    list_display_links = ["id"]
    list_editable = ["posts"]
    list_filter = ["year"]
    search_fields = ["year"]

    class Meta:
        model = PostArchive


class PostViewAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "date", "ip"]
    list_display_links = ["id"]
    list_filter = ["date", "post"]
    search_fields = ["ip"]

    class Meta:
        model = PostView


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "user"]
    list_display_links = ["id"]
    list_editable = ["post", "user"]
    list_filter = ["user"]

    class Meta:
        model = PostLike


admin.site.register(Post, PostModelAdmin)
admin.site.register(PostCategory, PostCategoryModelAdmin)
admin.site.register(PostImage, PostImageModelAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(PostArchive, PostArchiveAdmin)
admin.site.register(PostView, PostViewAdmin)
admin.site.register(PostLike, PostLikeAdmin)