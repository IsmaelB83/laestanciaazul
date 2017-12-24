# Python imports
# Django imports
from django.contrib import admin
# Third party app imports
# Local app imports
from .models import Post, Category, PostCategory, PostComment, PostImage


# More info here: https://docs.djangoproject.com/en/1.11/intro/tutorial07/
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "updated", "timestamp"]
    list_display_links = ["title"]
    list_editable = ["content"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "content"]
    class Meta:
        model = Post


class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ["id", "sort", "category", "css_class", "updated", "timestamp"]
    list_display_links = ["id"]
    list_editable = ["sort", "category", "css_class"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["category"]

    class Meta:
        model = Category


class PostCategoryModelAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "category"]
    list_display_links = ["id"]
    list_editable = ["post", "category"]
    list_filter = ["post", "category"]
    search_fields = ["post", "category"]

    class Meta:
        model = PostCategory


class PostCommentModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post", "num_comment", "comment", "timestamp", "updated"]
    list_display_links = ["id"]
    list_editable = ["comment", "post"]
    list_filter = ["user", "post"]
    search_fields = ["user", "post"]

    class Meta:
        model = PostComment


class PostImageModelAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "image", "timestamp"]
    list_display_links = ["id"]
    list_editable = ["post", "image"]
    list_filter = ["post"]
    search_fields = ["post"]

    class Meta:
        model = PostImage


admin.site.register(Post, PostModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(PostCategory, PostCategoryModelAdmin)
admin.site.register(PostComment, PostCommentModelAdmin)
admin.site.register(PostImage, PostImageModelAdmin)

# Admin is very good to model the application because it
# easily allow us to test the CRUD concept:#
#   CRUD:   Create* -- POST
#           Retrieve -- GET (Examples: List / Search)
#           Update* -- PUT/PATCH
#           Delete* -- DELETE
#
#  * They will require permnissons
