from django import forms

from .models import Post, PostComment, Category

CATEGORY_CHOICES = [[c.id, c.category] for c in Category.objects.all()]

class PostForm(forms.ModelForm):
    categorias_post = forms.MultipleChoiceField(choices=CATEGORY_CHOICES, required=False, widget=forms.CheckboxSelectMultiple, )
    title = forms.CharField(label="Title", required=True, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'title', 'autocomplete': 'off'}))

    class Meta:
        model = Post
        fields = ["categorias_post", "title", ]


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ["anonymous_name", "anonymous_email", "comment",
        ]


class LoginForm():
    user = forms.CharField(label="Username", required=True, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'username', 'autocomplete': 'off'}))
    password = forms.CharField(label="Password", required=True, max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'autocomplete': 'off'}))
