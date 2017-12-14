from django.contrib import admin

# Register your models here.
from .models import Post, Category, PostCategory, PostComment

# More info here: https://docs.djangoproject.com/en/1.11/intro/tutorial07/
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "num_comments", "updated", "timestamp"]
    list_display_links = ["title"]
    list_editable = ["content", "num_comments"]
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
    list_display = ["id", "num_comment", "user", "comment", "post", "num_likes", "timestamp", "updated"]
    list_display_links = ["id"]
    list_editable = ["comment", "post", "num_likes"]
    list_filter = ["user", "post"]
    search_fields = ["user", "post"]

    class Meta:
        model = PostCategory


admin.site.register(Post, PostModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(PostCategory, PostCategoryModelAdmin)
admin.site.register(PostComment, PostCommentModelAdmin)

# Admin is very good to model the application because it
# easily allow us to test the CRUD concept:#
#   CRUD:   Create* -- POST
#           Retrieve -- GET (Examples: List / Search)
#           Update* -- PUT/PATCH
#           Delete* -- DELETE
#
#  * They will require permnissons
