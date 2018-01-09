# coding=utf-8
# Python imports
# Django imports
from django import forms
from django.apps import apps
# Third party app imports
from multiupload.fields import MultiFileField
# Local app imports
from .models import Post, PostComment


CATEGORY_CHOICES = [[c.id, c.name] for c in apps.get_model('category', 'Category').objects.all()]


class PostForm(forms.ModelForm):
    postcategory = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        required=True,
        widget=forms.CheckboxSelectMultiple
    )
    status = forms.ChoiceField(choices=Post.STATUSES, required=True, widget=forms.RadioSelect)
    image_file = forms.FileField()
    postimage = MultiFileField(min_num=1, max_num=12, max_file_size=1024 * 1024)

    class Meta:
        model = Post
        fields = ('title', 'postcategory', 'status', 'published_date', 'image_file', 'content', 'postimage')


class PostFormEdit(forms.ModelForm):
    postcategory = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        required=True,
        widget=forms.CheckboxSelectMultiple
    )
    image_file = forms.FileField(required=False)
    postimage = MultiFileField(min_num=1, max_num=12, max_file_size=1024 * 1024, required=False)

    class Meta:
        model = Post
        fields = ('title', 'postcategory', 'status', 'published_date', 'image_file', 'content', 'postimage')
