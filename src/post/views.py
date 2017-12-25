# Python imports
# Django imports
from django.apps import apps
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# Third party app imports
# Local app imports
from .forms import PostForm, PostFormEdit
from .models import Post, PostImage, PostCategory, PostComment
from discuss.models import Comment
from gallery.models import Image
from user.models import UserProfile
from category.models import Category
from like.models import PostLike


def index_view(request):

    posts_all = Post.objects.all()[:15]
    paginator = Paginator(posts_all, 3)
    page_request_var = 'page'
    page = request.GET.get('page')
    
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    posts_cards = Post.objects.order_by('timestamp')[:3]
    posts_popular = Post.objects.annotate(comment_count=Count('postcomment__comment')).order_by('-comment_count')[:4]
    comments_recent = Comment.objects.order_by('-timestamp')[:4]
    pictures_recent = Image.objects.order_by('-timestamp')[:12]
    
    context = {
        'title': 'List of Posts',
        'posts': posts_page,
        'posts_cards': posts_cards,
        'posts_popular': posts_popular,
        'comments_recent': comments_recent,
        'pictures_recent': pictures_recent,
        'page_request': page_request_var,
    }
    
    return render(request, 'index.html', context)


def contact_view(request):
    return render(request, 'contact.html')


def archive_view(request):
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
        'title': 'List of Posts',
        'post': posts_page,
        'page_request': page_request_var
    }
    return render(request, 'archive.html', context)


def category_view(request, id):
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
    comments_recent = PostComment.objects.filter(post__in=posts_all).order_by('-comment__timestamp')[:4]
    pictures_recent = Image.objects.order_by('-timestamp')[:12]

    context = {
        'title': 'Category',
        'category': category,
        'posts': posts_page,
        'posts_popular': posts_popular,
        'comments_recent': comments_recent,
        'pictures_recent': pictures_recent,
        'page_request': page_request_var
    }
    return render(request, 'category.html', context)


def post_view(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.is_ajax():
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                if not PostLike.objects.filter(post=post, user=request.user, ip=ip).exists():
                    like = PostLike()
                    like.post = post
                    like.user = request.user
                    like.ip = ip
                    like.save()
                else:
                    like = PostLike.objects.filter(post=post, user=request.user, ip=ip)
                    like.delete()
            else:
                comment = Comment()
                comment.user = request.user
                comment.content = request.POST['comment']
                comment.save()
                post_comment = PostComment()
                post_comment.post = post
                post_comment.comment = comment
                post_comment.save()
                messages.success(request, 'Comentario añadido')
        else:
            messages.error(request, 'Es necesario hacer log in para dar un like')

    posts_popular = Post.objects.annotate(comment_count=Count('postcomment__comment')).order_by('-comment_count')[:4]
    pictures_recent = Image.objects.order_by('-timestamp')[:12]
    already_like = "False"
    if request.user.is_authenticated:
        already_like = PostLike.objects.filter(post=post, user=request.user).exists()

    context = {
        'title': post.title,
        'posts_popular': posts_popular,
        'pictures_recent': pictures_recent,
        'already_like': already_like,
        'post': post,
    }
    return render(request, 'post.html', context)


def post_create_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = Image()
                image.caption = form.cleaned_data['image_file'].name
                image.image = form.cleaned_data['image_file']
                image.save()
                post = form.save(commit=False)
                post.author = UserProfile.objects.get(user=request.user)
                post.image = image
                post.save()
                for category in form.cleaned_data['postcategory']:
                    post_category = PostCategory()
                    post_category.post = post
                    post_category.category = apps.get_model('category', 'Category').objects.get(id=category)
                    post_category.save()
                for file_image in form.cleaned_data['postimage']:
                    image = Image()
                    image.caption = file_image.name
                    image.image = file_image
                    image.save()
                    post_image = PostImage()
                    post_image.post = post
                    post_image.image = image
                    post_image.save()
                messages.success(request, 'Successfully created')
                return redirect('blog:index')
        else:
            form = PostForm()

        context = {
            'title': 'Create post',
            'form': form,
        }

        return render(request, 'post_form.html', context)
    else:
        messages.error(request, 'Not authenticated')
        return redirect('blog:index')


def post_edit_view(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        form = PostFormEdit(request.POST or None, request.FILES or None, instance=post)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                for postC in PostCategory.objects.filter(post=post):
                    postC.delete()
                for category in form.cleaned_data['postcategory']:
                    post_category = PostCategory()
                    post_category.post = post
                    post_category.category = apps.get_model('category', 'Category').objects.get(id=category)
                    post_category.save()
                for image in PostImage.objects.filter(post=post):
                    image.delete()
                for image in form.cleaned_data['postimage']:
                    post_image = PostImage()
                    post_image.post = post
                    post_image.image = image
                    post_image.caption = image.name
                    post_image.save()
                messages.success(request, 'Successfully created')
                return redirect('blog:index')

        context = {
            'title': 'Edit post',
            'post': post,
            'form': form,
        }

        return render(request, 'post_form.html', context)
    else:
        messages.error(request, 'Not authenticated')
        return redirect('blog:index')