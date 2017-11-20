from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^create/$',views.posts_create, name='post_create'),
    url(r'^detail/$', views.posts_detail, name='post_detail'),
    url(r'^list/$', views.posts_list, name='post_list'),
    url(r'^update/$', views.posts_update, name='post_update'),
    url(r'^delete/$', views.posts_delete, name='post_delete'),
]

