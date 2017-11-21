from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import Post
from .forms import PostForm

# Create your views here.
def posts_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        messages.success(request, "Successfully created", extra_tags="some-tag success")
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


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
    return render(request, "index.html", context)


def posts_update(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        messages.success(request, "<a href=''>Item saved</a>", extra_tags="html_seguro")
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        "title": post.title,
        "post": post,
        "form": form,
    }
    return render(request, "post_form.html", context)

def posts_delete(request):
    return HttpResponse("<h1>DELETE</h1")
