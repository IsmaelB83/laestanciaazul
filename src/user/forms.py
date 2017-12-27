# Python imports
# Django imports
from django import forms
# Third party app imports
# Local app imports
from .models import UserProfile


class LoginForm(forms.ModelForm):
    user = forms.CharField(label='Username', required=True, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'username', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', required=True, max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'autocomplete': 'off'}))


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50, required=False)
    user_id = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)

    class Meta:
        model = UserProfile
        fields = ('user_id', 'first_name', 'last_name', 'email', 'location', 'description', 'image', 'author')