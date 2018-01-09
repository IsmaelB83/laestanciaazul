# coding=utf-8
# Python imports
# Django imports
# Third party app imports
# Local app imports
from .forms import LoginForm


def login_form(request):
    return {
        'login_form': LoginForm(),
    }
