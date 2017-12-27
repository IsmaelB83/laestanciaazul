# Python imports
# Django imports
from django.contrib import admin
# Third party app imports
# Local app imports
from .models import Post, PostCategory, PostImage, PostComment, PostArchive


# More info here: https://docs.djangoproject.com/en/1.11/intro/tutorial07/
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "published_date", "updated", "timestamp"]
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


admin.site.register(Post, PostModelAdmin)
admin.site.register(PostCategory, PostCategoryModelAdmin)
admin.site.register(PostImage, PostImageModelAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(PostArchive, PostArchiveAdmin)


# Admin is very good to model the application because it
# easily allow us to test the CRUD concept:#
#   CRUD:   Create* -- POST
#           Retrieve -- GET (Examples: List / Search)
#           Update* -- PUT/PATCH
#           Delete* -- DELETE
#
#  * They will require permnissons
