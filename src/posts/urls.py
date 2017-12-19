from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.contact, name='contact'), url(r'^archive/$', views.archive, name='archive'), url(r'^category/(?P<id>all|prog|rpi|linux|sap|other)/$', views.category, name='category'),
    url(r'^post/(?P<id>\d+)/$', views.post_view, name='post'), url(r'^post/create/$', views.post_create, name='post_create'), url(r'^post/edit/(?P<id>\d+)/$', views.post_edit, name='post_edit'),
    url(r'^profile/(?P<id>\d+)/$', views.profile, name='profile'),
]

#   url(r'^post/(?P<id>\d+)/$', views.posts_detail, name='detail'),
#   url(r'^list/$', views.posts_list, name='list'),
#   url(r'^(?P<id>\d+)/edit/$', views.posts_update, name='update'),
#   url(r'^(?P<id>\d+)/delete/$', views.posts_delete, name='delete'),
