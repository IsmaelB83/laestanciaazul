from django import forms
from django.utils.html import strip_tags
from multiupload.fields import MultiFileField

from .models import Post, PostComment, Category, SocialProfile, User

CATEGORY_CHOICES = [[c.id, c.category] for c in Category.objects.all()]


class PostForm(forms.ModelForm):
    postcategory = forms.MultipleChoiceField(choices=CATEGORY_CHOICES, required=True, widget=forms.CheckboxSelectMultiple, )
    status = forms.ChoiceField(choices=Post.STATUSES, required=True, widget=forms.RadioSelect, )
    postimage = MultiFileField(min_num=0, max_num=100, max_file_size=1024 * 1024)

    class Meta:
        model = Post
        fields = ('title', 'postcategory', 'status', 'published_date', 'image', 'content', 'postimage')


class PostFormEdit(forms.ModelForm):
    postcategory = forms.MultipleChoiceField(choices=CATEGORY_CHOICES, required=True, widget=forms.CheckboxSelectMultiple, )
    postimage = MultiFileField(min_num=0, max_num=100, max_file_size=1024 * 1024)

    class Meta:
        model = Post
        fields = ('title', 'postcategory', 'status', 'published_date', 'image', 'content', 'postimage')


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['anonymous_name', 'anonymous_email', 'comment', ]


class LoginForm():
    user = forms.CharField(label='Username', required=True, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'username', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', required=True, max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'autocomplete': 'off'}))


class UserForm(forms.ModelForm):
    """Form for editing the data that is part of the User model"""

    class Meta(object):
        """Configuration for the ModelForm"""
        model = User
        fields = {'username', 'first_name', 'last_name', 'email'}


class SocialProfileForm(forms.ModelForm):
    """Master form for editing the user's profile"""

    user = forms.IntegerField(widget=forms.HiddenInput, required=True)
    returnTo = forms.CharField(widget=forms.HiddenInput, required=False, initial='/')  # URI to Return to after save
    manually_edited = forms.BooleanField(widget=forms.HiddenInput, required=False, initial=True)

    class Meta(object):
        """Configuration for the ModelForm"""
        model = SocialProfile
        fields = {'user', 'gender', 'url', 'image_url',
                  'description'}  # Don't let through for security reasons, user should be based on logged in user only

    def clean_description(self):
        """Automatically called by Django, this method 'cleans' the description, e.g. stripping HTML out of desc"""
        return strip_tags(self.cleaned_data['description'])

    def clean(self):
        """Automatically called by Django, this method 'cleans' the whole form"""
        if self.changed_data:
            self.cleaned_data['manually_edited'] = True
