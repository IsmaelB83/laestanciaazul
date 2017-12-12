from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
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
        "page_obj": posts_page,
        "page_request_var": page_request_var
    }
    return render(request, "index.html", context)


def contact(request):
    return render(request, "contact.html")


def archive(request):
    return render(request, "archive.html")


def posts_detail(request, id):
    post = get_object_or_404(Post, id=id)
    context = {
        "title": post.title,
        "post": post,
    }
    return render(request, "post.html", context)


def category(request, id):
    categorias = {
        'all': 'TODO',
        'prog': 'PROGRAMACIÓN',
        'rpi': 'RASPBERY PI',
        'linux': 'LINUX',
        'sap': 'SAP',
        'other': 'OTROS'
    }
    categoria = categorias[id]
    context = {
        'title': "Category",
        'category': categoria
    }
    return render(request, "category.html", context)


def posts_create(request, category):

    if request.user.is_authenticated:
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Successfully created")
            return redirect("blog:list")

        context = {
            "form": form,
            "title": "Create new post"
        }
        return render(request, "post_form.html", context)
    else:
        messages.error(request, "Not authenticated")
        return redirect("blog:list")

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
            return redirect("blog:list")

        context = {
            "title": "Edit post: " + post.title,
            "post": post,
            "form": form,
        }
        return render(request, "post_form.html", context)
    else:
        messages.error(request, "Not authenticated")
        return redirect("blog:list")

def posts_delete(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        post.delete()
        messages.success(request, "Successfully deleted")
    else:
        messages.error(request, "Not authenticated")
    return redirect("blog:list")
