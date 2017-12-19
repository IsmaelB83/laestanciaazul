from django import forms

from .models import Post, PostComment, Category

CATEGORY_CHOICES = [[c.id, c.category] for c in Category.objects.all()]


class PostForm(forms.ModelForm):
    postcategory = forms.MultipleChoiceField(choices=CATEGORY_CHOICES, required=True, widget=forms.CheckboxSelectMultiple, )
    status = forms.ChoiceField(choices=Post.STATUSES, required=True, widget=forms.RadioSelect, )

    class Meta:
        model = Post
        fields = ('title', 'postcategory', 'status', 'published_date', 'image', 'content')


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['anonymous_name', 'anonymous_email', 'comment', ]


class LoginForm():
    user = forms.CharField(label='Username', required=True, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'username', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', required=True, max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'autocomplete': 'off'}))
