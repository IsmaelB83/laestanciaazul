from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from .models import Post, Category, PostComment, Author, PostImage, PostCategory
from .forms import PostForm, PostCommentForm

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

    posts_popular = Post.objects.annotate(comment_count=Count('postcomment__comment')).order_by('-comment_count')[:4]
    comments_recent = PostComment.objects.order_by('-timestamp')[:4]
    pictures_recent = PostImage.objects.order_by('-timestamp')[:12]

    context = {'title': 'List of Posts', 'posts': posts_page, 'posts_popular': posts_popular, 'comments_recent': comments_recent, 'pictures_recent': pictures_recent, 'page_request': page_request_var,
    }
    return render(request, 'index.html', context)


def contact(request):
    return render(request, 'contact.html')


def profile(request, id):
    author = get_object_or_404(Author, id=id)
    context = {'author': author}
    return render(request, 'profile.html', context)


def archive(request):
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
    context = {'title': 'List of Posts', 'posts': posts_page, 'page_request': page_request_var
    }
    return render(request, 'archive.html', context)


def category(request, id):
    try:
        category = Category.objects.get(id=id)
        if id != 'all' and category:
            posts_all = Post.objects.filter(postcategory__category=category)
        else:
            posts_all = Post.objects.all()
    except ObjectDoesNotExist:
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

    posts_popular = posts_all.annotate(comment_count=Count('postcomment__comment')).order_by('-comment_count')[:4]
    comments_recent = PostComment.objects.filter(post__in=posts_all).order_by('-timestamp')[:4]
    pictures_recent = PostImage.objects.filter(post__in=posts_all).order_by('-timestamp')[:12]

    context = {'title': 'Category', 'category': category, 'posts': posts_page, 'posts_popular': posts_popular, 'comments_recent': comments_recent, 'pictures_recent': pictures_recent,
        'page_request': page_request_var
    }
    return render(request, 'category.html', context)


def post_view(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        if request.is_ajax():
            post.num_likes = post.num_likes + 1
            post.save()
        else:
            form = PostCommentForm(request.POST)
            if form.is_valid():
                post_comment = form.save(commit=False)
                if request.user.is_authenticated:
                    post_comment.author = request.user.author
                post_comment.post = post
                try:
                    post_comment.num_comment = post.postcomment_set.latest('num_comment').num_comment + 1
                except ObjectDoesNotExist:
                    post_comment.num_comment = 1
                post_comment.save()
                messages.success(request, 'Comentario añadido')

    posts_popular = Post.objects.annotate(comment_count=Count('postcomment__comment')).order_by('-comment_count')[:4]
    pictures_recent = PostImage.objects.order_by('-timestamp')[:12]

    context = {'title': post.title, 'posts_popular': posts_popular, 'pictures_recent': pictures_recent, 'post': post, }
    return render(request, 'post.html', context)


def post_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = Author.objects.get(user=request.user)
                post.num_likes = 0
                post.save()
                for aux in form.cleaned_data['postcategory']:
                    post_category = PostCategory()
                    post_category.post = post
                    post_category.category = Category.objects.get(id=aux)
                    post_category.save()
                messages.success(request, 'Successfully created')
                return redirect('blog:index')
        else:
            form = PostForm()

        context = {"title": "Create post", "form": form, }

        return render(request, 'post_form.html', context)
    else:
        messages.error(request, 'Not authenticated')
        return redirect('blog:index')


def post_edit(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        form = PostForm(request.POST or None, request.FILES or None, instance=post)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                for postC in PostCategory.objects.filter(post=post):
                    postC.delete()
                for aux in form.cleaned_data['postcategory']:
                    post_category = PostCategory()
                    post_category.post = post
                    post_category.category = Category.objects.get(id=aux)
                    post_category.save()
                messages.success(request, 'Successfully created')
                return redirect('blog:index')

        context = {"title": "Edit post", "post": post, "form": form, }

        return render(request, 'post_form.html', context)
    else:
        messages.error(request, 'Not authenticated')
        return redirect('blog:index')
