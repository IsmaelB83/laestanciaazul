# Python imports
# Django imports
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# Third party app imports
from social_django.models import UserSocialAuth
# Local app imports
from .models import Author


# Create your views here.
def profile(request, id):
    # Recuperar usuario y autor asociado
    author = get_object_or_404(Author, id=id)
    # El perfil a buscar es el del usuario logueado?
    current_user = request.user
    if current_user == author.user:
        try:
            github_login = current_user.social_auth.get(provider='github')
        except UserSocialAuth.DoesNotExist:
            github_login = None
        try:
            twitter_login = current_user.social_auth.get(provider='twitter')
        except UserSocialAuth.DoesNotExist:
            twitter_login = None
        try:
            facebook_login = current_user.social_auth.get(provider='facebook')
        except UserSocialAuth.DoesNotExist:
            facebook_login = None
        # Sólo puede desconectar red social si ha introducido password
        can_disconnect = (current_user.social_auth.count() > 1 or current_user.has_usable_password())
    else:
        github_login = None
        twitter_login = None
        facebook_login = None
        can_disconnect = False
    # Contexto y render
    context = {
        'author': author,
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    }
    return render(request, 'profile.html', context)


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm
    
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('blog:index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    
    context = {'form': form}
    
    return render(request, 'password.html', context)
