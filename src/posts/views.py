from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm

# Create your views here.
def posts_create(request):
    if request.user.is_authenticated:
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Successfully created")
            return redirect("posts:list")

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
    posts_all = Post.objects.all()
    paginator = Paginator(posts_all, 3)
    page_request_var = 'page'
    page = request.GET.get('page')
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)
    context = {
        "title": "List of Posts",
        "posts": posts_page,
        "page_request_var": page_request_var
    }
    return render(request, "post_list.html", context)

def posts_update(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        form = PostForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, "<a href=''>Item saved</a>", extra_tags="html_seguro")
            return redirect("posts:list")

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
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        post.delete()
        messages.success(request, "Successfully deleted")
    else:
        messages.error(request, "Not authenticated")
    return redirect("posts:list")
