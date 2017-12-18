from .models import Category, Post, PostComment
from .forms import LoginForm

def categories(request):
    categories = Category.objects.filter(sort__gt=0)
    return {'categories': categories}


def login_form(request):
    return {'login_form': LoginForm(), }
