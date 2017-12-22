from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.views.generic import DeleteView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from .forms import PostForm, PostFormEdit, PostCommentForm, SocialProfileForm, UserForm
from .models import Post, Category, PostComment, Author, PostImage, PostCategory, User


# Create your views here.
def index(request):
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
    comments_recent = PostComment.objects.order_by('-timestamp')[:4]
    pictures_recent = PostImage.objects.order_by('-timestamp')[:12]

    context = {'title': 'List of Posts', 'posts': posts_page, 'posts_cards': posts_cards, 'posts_popular': posts_popular,
        'comments_recent': comments_recent, 'pictures_recent': pictures_recent, 'page_request': page_request_var,
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

    context = {'title': 'Category', 'category': category, 'posts': posts_page, 'posts_popular': posts_popular, 'comments_recent': comments_recent,
        'pictures_recent': pictures_recent,
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
                for category in form.cleaned_data['postcategory']:
                    post_category = PostCategory()
                    post_category.post = post
                    post_category.category = Category.objects.get(id=category)
                    post_category.save()
                for image in form.cleaned_data['postimage']:
                    post_image = PostImage()
                    post_image.post = post
                    post_image.image = image
                    post_image.caption = image.name
                    post_image.save()

                messages.success(request, 'Successfully created')
                return redirect('blog:index')
        else:
            form = PostForm()

        context = {'title': 'Create post', 'form': form, }

        return render(request, 'post_form.html', context)
    else:
        messages.error(request, 'Not authenticated')
        return redirect('blog:index')


def post_edit(request, id):
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
                    post_category.category = Category.objects.get(id=category)
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

        context = {'title': 'Edit post', 'post': post, 'form': form, }

        return render(request, 'post_form.html', context)
    else:
        messages.error(request, 'Not authenticated')
        return redirect('blog:index')


DEFAULT_RETURNTO_PATH = getattr(settings, 'DEFAULT_RETURNTO_PATH', '/')


class SelectAuthView(TemplateView):
    """
    Lets users choose how they want to request access.
    url: /select
    """
    template_name = 'socialprofile/sp_account_select.html'

    def get_context_data(self, **kwargs):
        """Ensure that 'next' gets passed along"""
        next_url = self.request.GET.get(REDIRECT_FIELD_NAME, DEFAULT_RETURNTO_PATH)
        context = super(SelectAuthView, self).get_context_data(**kwargs)
        context['next_param'] = REDIRECT_FIELD_NAME
        context['next_url'] = next_url
        return context


class SocialProfileView(TemplateView):
    """
    Profile View Page
    url: /profile/view
    """
    template_name = 'socialprofile/sp_profile_view.html'

    http_method_names = {'get'}

    def get_context_data(self, **kwargs):
        """Load up the default data to show in the display form."""
        username = self.kwargs.get('username')
        if username:
            user = get_object_or_404(User, username=username)
        elif self.request.user.is_authenticated():
            user = self.request.user
        else:
            raise Http404  # Case where user gets to this view anonymously for non-existent user

        return_to = self.request.GET.get('returnTo', DEFAULT_RETURNTO_PATH)

        sp_form = SocialProfileForm(instance=user.social_profile)
        user_form = UserForm(instance=user)

        sp_form.initial['returnTo'] = return_to

        return {'sp_form': sp_form, 'user_form': user_form}


class SocialProfileEditView(SocialProfileView):
    """
    Profile Editing View
    url: /profile/edit
    """

    template_name = 'socialprofile/sp_profile_edit.html'

    http_method_names = {'get', 'post'}

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        sp_form = SocialProfileForm(request.POST, instance=request.user.social_profile)

        if user_form.is_valid() & sp_form.is_valid():
            user_form.save()
            sp_form.save()
            messages.add_message(self.request, messages.INFO, _('Your profile has been updated.'))
            return HttpResponseRedirect(sp_form.cleaned_data.get('returnTo', DEFAULT_RETURNTO_PATH))
        else:
            messages.add_message(self.request, messages.INFO, _('Your profile has NOT been updated.'))
            return self.render_to_response({'sp_form': sp_form, 'user_form': user_form})


class DeleteSocialProfileView(DeleteView):
    """
    Account Delete Confirm Modal View
    url: /delete
    """
    success_url = reverse_lazy('sp_logout_page')
    template_name = "socialprofile/sp_delete_account_modal.html"
    model = User

    def get_object(self, queryset=None):
        """Get the object that we are going to delete"""
        return self.request.user
