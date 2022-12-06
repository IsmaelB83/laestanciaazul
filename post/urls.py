# coding=utf-8
# Python imports
# Django imports
from django.urls import re_path
# Third party app imports
# Local app imports
from . import views


urlpatterns = [
    re_path(r'^$', views.index_view, name='index'),
    re_path(r'^gallery/$', views.gallery_view, name='gallery'),
    re_path(r'^archive/(?P<year>\d+)/(?P<month>\d+)/$', views.archive_view, name='archive'),
    re_path(r'^category/(?P<id>[\w]+)/$', views.category_view, name='category'),
    re_path(r'^search/(?P<filter>[\w\-]+)/$', views.search_view, name='search'),
    re_path(r'^post/create/$', views.post_create_view, name='post_create'),
    re_path(r'^post/(?P<id>[\w\-]+)/$', views.post_view, name='post'),
    re_path(r'^post/like/(?P<id>[\w\-]+)$', views.post_like_view, name='post_like'),
    re_path(r'^post/edit/(?P<id>[\w\-]+)/$', views.post_edit_view, name='post_edit'),
    re_path(r'^post/delete/(?P<id>[\w\-]+)/$', views.post_delete_view, name='post_delete'),

]