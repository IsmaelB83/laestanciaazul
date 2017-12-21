from django import forms
from multiupload.fields import MultiFileField

from .models import Post, PostComment, Category

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
