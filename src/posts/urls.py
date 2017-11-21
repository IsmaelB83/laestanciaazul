from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^create/$', views.posts_create),
    url(r'^(?P<id>\d+)/$', views.posts_detail, name='detail'),
    url(r'^list/$', views.posts_list),
    url(r'^(?P<id>\d+)/edit/$', views.posts_update),
    url(r'^delete/$', views.posts_delete),
]

