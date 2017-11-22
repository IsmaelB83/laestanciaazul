from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from .forms import PostForm

# Create your views here.
def posts_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        if request.user.is_authenticated:
            post = form.save(commit=False)
            post.save()
            messages.success(request, "Successfully created")
        else:
            messages.error(request, "Not authenticated")
        return redirect("posts:list")

    if request.user.is_authenticated:
        context = {
            "form": form,
            "title": "Create new post"
        }
        return render(request, "post_form.html", context)
    else:
        messages.error(request, "Not authenticated")
        return redirect("posts:list")


def posts_detail(request, id):
    post = get_object_or_404(Post, id=id)
    context = {
        "title": post.title,
        "post": post,
    }
    return render(request, "post_detail.html", context)


def posts_list(request):
    posts = Post.objects.all()
    context = {
        "title": "List",
        "posts": posts
    }
    return render(request, "post_list.html", context)


def posts_update(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        if request.user.is_authenticated:
            post = form.save(commit=False)
            post.save()
            messages.success(request, "<a href=''>Item saved</a>", extra_tags="html_seguro")
        else:
            messages.error(request, "Not authenticated")
        return redirect("posts:list")

    if request.user.is_authenticated:
        context = {
            "title": "Edit post: " + post.title,
            "post": post,
            "form": form,
        }
        return render(request, "post_form.html", context)
    else:
        messages.error(request, "Not authenticated")
        return redirect("posts:list")


def posts_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user.is_authenticated:
        post.delete()
        messages.success(request, "Successfully deleted")
    else:
        messages.error(request, "Not authenticated")
    return redirect("posts:list")
