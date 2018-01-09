# coding=utf-8
# Python imports
# Django imports
# Third party app imports
# Local app imports
from .models import Category


def categories_pre_proc (request):
    categories = Category.objects.filter(sort__gt=0)
    return {
        'categories': categories
    }
