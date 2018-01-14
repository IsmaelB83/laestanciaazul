# coding=utf-8
# Python imports
# Django imports
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
# Third party app imports
from social_django.models import UserSocialAuth
# Local app imports
from discuss.models import Comment
from history.models import LogUser
from like.models import PostLike
from post.models import Post
from .models import UserProfile, UserFollow
from .forms import ProfileForm


@login_required
def user_register_view(request):
    # Se obtiene el perfil del usuario, o si no existe se crea uno nuevo
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile()
        profile.user = request.user
    # Recupero todos los perfiles disponibles
    try:
        github_login = profile.user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    try:
        twitter_login = profile.user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None
    try:
        facebook_login = profile.user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None
    try:
        google_login = profile.user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None
    # Sólo puede desconectar red social si ha introducido password o si tengo varios conec
    can_disconnect = (profile.user.social_auth.count() > 1 or profile.user.has_usable_password())
    # Evento POST
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            old_image = profile.image
            old_author = profile.author
            profile = form.save(commit=False)
            profile.user = request.user
            profile.user.first_name = form.cleaned_data['first_name']
            profile.user.last_name = form.cleaned_data['last_name']
            profile.user.email = form.cleaned_data['email']
            if not profile.image:
                profile.image = old_image
            profile.author = old_author
            profile.user.save()
            profile.save()
            profile.add_log(profile, "edit")
            messages.success(request, 'Tus datos de usuario han sido actualizados')
            return redirect('blog:index')
    else:
        form = ProfileForm(instance=profile, initial={
            'user_id': profile.user.username,
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'email': profile.user.email,
        })

    # Generamos el contexto
    context = {
        'form': form,
        'profile': profile,
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'google_login': google_login,
        'can_disconnect': can_disconnect
    }

    # Renderizamos el template del edición del perfil
    return render(request, 'user/register.html', context)


# Create your views here.
def about_user_view(request, id):
    # Recuperar mi usuario
    try:
        user = User.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.error(request, 'El usuario no existe')
        return redirect('blog:index')
    # Registro la visita del usuario
    if request.user.is_authenticated and request.user.userprofile:
        request.user.userprofile.add_log(user.userprofile, "visit")
    # Recuperar datos adicionales del usuario
    posts_user = Post.objects.filter(author__user=user)
    comments_user = Comment.objects.filter(user=user)
    post_likes = PostLike.objects.filter(user=user)
    follows = UserFollow.objects.filter(user=user)
    followers = UserFollow.objects.filter(follows=user)
    log_user = LogUser.objects.filter(user=user).order_by('-timestamp')
    # Contexto y render
    context = {
        'profile': user.userprofile,
        'posts_user': posts_user,
        'comments_user': comments_user,
        'post_likes': post_likes,
        'follows': follows,
        'followers': followers,
        'log_user': log_user,
    }
    return render(request, 'user/about_user.html', context)

@login_required
def password(request):
    if request.user.has_usable_password():
        password_form = PasswordChangeForm
    else:
        password_form = AdminPasswordChangeForm
    
    if request.method == 'POST':
        form = password_form(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('blog:index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = password_form(request.user)
    
    context = {'form': form}
    
    return render(request, 'user/password.html', context)
