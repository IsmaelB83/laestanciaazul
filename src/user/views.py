# Python imports
# Django imports
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
# Third party app imports
from social_django.models import UserSocialAuth
# Local app imports
from .models import UserProfile
from .forms import ProfileForm


# Create your views here.
def profile(request, id):
    # Recuperar usuario y autor asociado
    profile = get_object_or_404(UserProfile, id=id)
    # El perfil a buscar es el del usuari   o logueado?
    if profile.user == request.user:
        try:
            github_login = profile.social_auth.get(provider='github')
        except UserSocialAuth.DoesNotExist:
            github_login = None
        try:
            twitter_login = profile.social_auth.get(provider='twitter')
        except UserSocialAuth.DoesNotExist:
            twitter_login = None
        try:
            facebook_login = profile.social_auth.get(provider='facebook')
        except UserSocialAuth.DoesNotExist:
            facebook_login = None
        # Sólo puede desconectar red social si ha introducido password
        can_disconnect = (profile.social_auth.count() > 1 or profile.has_usable_password())
    else:
        github_login = None
        twitter_login = None
        facebook_login = None
        can_disconnect = False
    # Contexto y render
    context = {
        'profile': profile,
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    }
    return render(request, 'user/profile.html', context)


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


@login_required
def register(request):
    # Salvar los datos
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile()
        profile.user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.is_staff = False
            request.user.email = form.cleaned_data['email']
            request.user.save()
            request.user.profile = form.save(commit=False)
            request.user.profile.id = profile.id
            if profile.id:
                request.user.profile.save(force_update=True)
            else:
                request.user.profile.save()
            messages.success(request, 'Your data has been updated!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    
    return render(request, 'user/register.html', context)
