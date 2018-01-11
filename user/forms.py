# coding=utf-8
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
    user_id = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'your username...', 'maxlength': '30'}),
        max_length=150
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "your name..."}),
        max_length=30)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "your lastname..."}),
        max_length=30,
        required=False
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': "your e-mail..."}),
        max_length=50,
    )
    country = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "your country..."}),
        max_length=20,
        required=False
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "your city..."}),
        max_length=30,
        required=False
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "short description about you..."}),
        max_length=100,
        required=True
    )
    image = forms.ImageField(
        required=False
    )
    
    class Meta:
        model = UserProfile
        fields = ('user_id', 'first_name', 'last_name', 'email', 'country', 'location',
                  'description', 'image')

    # def clean(self):
    #     cleaned_data = super(ProfileForm, self).clean()
    #     description = cleaned_data.get('description')
    #     if not description:
    #         raise forms.ValidationError('You have a description!')
