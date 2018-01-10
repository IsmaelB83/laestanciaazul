# coding=utf-8
#  Python imports
# Django imports
from django.shortcuts import render, redirect


# Third party app imports
# Local app imports


def error_404(request):
    return render(request, 'not_found.html', {})


def error_500(request):
    return render(request, 'not_found.html', {})
