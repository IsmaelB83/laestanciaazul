# Python imports
# Django imports
# Third party app imports
# Local app imports
from .models import Category, Post, PostComment


def categories(request):
    categories = Category.objects.filter(sort__gt=0)
    return {
        'categories': categories
    }
