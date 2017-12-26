# Python imports
# Django imports
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
# Third party app imports
from social_django.models import UserSocialAuth
# Local app imports
from .models import UserProfile
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

    # Sólo puede desconectar red social si ha introducido password
    can_disconnect = (profile.user.social_auth.count() > 1 or profile.user  .has_usable_password())

    # Evento POST
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.user.first_name = form.cleaned_data['first_name']
            profile.user.last_name = form.cleaned_data['last_name']
            profile.user.email = form.cleaned_data['email']
            profile.user.save()
            profile.save()
            messages.success(request, 'Tus datos de usuario han sido actualizados')
            return redirect('blog:index')
        else:
            messages.error(request, 'Corrige los errores indicados')
    else:
        form = ProfileForm(instance=profile)

    # Generamos el contexto
    context = {
        'form': form,
        'profile': profile,
        'github_login': github_login,
        'twitter_login': twitter_login,
        'can_disconnect': can_disconnect
    }

    # Renderizamos el template del edición del perfil
    return render(request, 'user/register.html', context)


# Create your views here.
def about_user_view(request, id):
    # Recuperar usuario y autor asociado
    user = get_object_or_404(User, id=id)
    # Contexto y render
    context = {
        'profile': user.userprofile,
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
