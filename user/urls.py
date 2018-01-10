# coding=utf-8
# Python imports
# Django imports
from django.conf.urls import url
# Third party app imports
# Local app imports
from . import views


urlpatterns = [
    url(r'^profile/(?P<id>[\w]+)/$', views.about_user_view, name='profile'),
    url(r'^password/$', views.password, name='password'),
    url(r'^register/$', views.user_register_view, name='register'),
]
