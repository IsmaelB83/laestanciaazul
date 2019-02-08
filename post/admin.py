# coding=utf-8
# Python imports
# Django imports
from django.contrib import admin
# Third party app imports
# Local app imports
from .models import Post, PostCategory, PostImage, PostImageSmall, PostComment, PostArchive, PostView, PostLike


# More info here: https://docs.djangoproject.com/en/1.11/intro/tutorial07/
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "content", "published_date", "updated", "timestamp"]
    list_display_links = ["title"]
    list_editable = ["content"]
    list_filter = ["published_date", "updated", "timestamp"]
    search_fields = ["published_date", "title", "content"]

    class Meta:
        model = Post


class PostCategoryModelAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "category"]
    list_display_links = ["id"]
    list_editable = ["post", "category"]
    list_filter = ["post", "category"]
    search_fields = ["post", "category"]

    class Meta:
        model = PostCategory


class PostImageModelAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "image"]
    list_display_links = ["id"]
    list_editable = ["post", "image"]
    list_filter = ["post"]
    search_fields = ["post"]

    class Meta:
        model = PostImage


class PostImageSmallModelAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "image"]
    list_display_links = ["id"]
    list_editable = ["post", "image"]
    list_filter = ["post"]
    search_fields = ["post"]
    
    class Meta:
        model = PostImageSmall


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "comment"]
    list_display_links = ["id"]
    list_editable = ["post", "comment"]
    list_filter = ["post"]
    search_fields = ["post"]

    class Meta:
        model = PostComment


class PostArchiveAdmin(admin.ModelAdmin):
    list_display = ["id", "year", "month", "posts"]
    list_display_links = ["id"]
    list_editable = ["posts"]
    list_filter = ["year", "month"]
    search_fields = ["year", "month"]

    class Meta:
        model = PostArchive


class PostViewAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "date", "ip"]
    list_display_links = ["id"]
    list_editable = ["post", "ip"]
    list_filter = ["post", "date"]
    search_fields = ["post", "date", "ip"]

    class Meta:
        model = PostView


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "date", "user"]
    list_display_links = ["id"]
    list_editable = ["post", "user"]
    list_filter = ["post", "date"]
    search_fields = ["post", "date", "user"]

    class Meta:
        model = PostLike


admin.site.register(Post, PostModelAdmin)
admin.site.register(PostCategory, PostCategoryModelAdmin)
admin.site.register(PostImage, PostImageModelAdmin)
admin.site.register(PostImageSmall, PostImageSmallModelAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(PostArchive, PostArchiveAdmin)
admin.site.register(PostView, PostViewAdmin)
admin.site.register(PostLike, PostLikeAdmin)


# Admin is very good to model the application because it
# easily allow us to test the CRUD concept:#
#   CRUD:   Create* -- POST
#           Retrieve -- GET (Examples: List / Search)
#           Update* -- PUT/PATCH
#           Delete* -- DELETE
#
#  * They will require permnissons
