# Python imports
# Django imports
from django import forms
from django.apps import apps
# Third party app imports
from multiupload.fields import MultiFileField
# Local app imports
from .models import Post


#CATEGORY_CHOICES = [[c.id, c.category] for c in apps.get_model('category', 'Category').objects.all()]


class PostForm(forms.ModelForm):
    #choices = CATEGORY_CHOICES,
    postcategory = forms.MultipleChoiceField( required=True, widget=forms.CheckboxSelectMultiple, )
    status = forms.ChoiceField(choices=Post.STATUSES, required=True, widget=forms.RadioSelect, )
    postimage = MultiFileField(min_num=0, max_num=100, max_file_size=1024 * 1024)

    class Meta:
        model = Post
        fields = ('title', 'postcategory', 'status', 'published_date', 'image', 'content', 'postimage')


class PostFormEdit(forms.ModelForm):
    #choices=CATEGORY_CHOICES,
    postcategory = forms.MultipleChoiceField( required=True, widget=forms.CheckboxSelectMultiple, )
    postimage = MultiFileField(min_num=0, max_num=100, max_file_size=1024 * 1024)

    class Meta:
        model = Post
        fields = ('title', 'postcategory', 'status', 'published_date', 'image', 'content', 'postimage')


