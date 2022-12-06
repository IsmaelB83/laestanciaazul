# coding=utf-8
# Python imports
# Django imports
from django.urls import re_path
# Third party app imports
# Local app imports
from . import views


urlpatterns = [
    re_path(r'^profile/(?P<id>[\w]+)/$', views.about_user_view, name='profile'),
    re_path(r'^password/$', views.password, name='password'),
    re_path(r'^register/$', views.user_register_view, name='register'),
]
