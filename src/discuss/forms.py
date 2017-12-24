# Python imports
# Django imports
from django import forms
# Third party app imports
# Local app imports
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', ]