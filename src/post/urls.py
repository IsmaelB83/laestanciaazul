# Python imports
# Django imports
from django.conf.urls import url
# Third party app imports
# Local app imports
from . import views


urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^gallery/$', views.gallery_view, name='gallery'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)/$', views.archive_view, name='archive'),
    url(r'^category/(?P<id>[\w]+)/$', views.category_view, name='category'),
    url(r'^search/(?P<filter>[\w\-]+)/$', views.search_view, name='search'),
    url(r'^post/(?P<id>\d+)/$', views.post_view, name='post'),
    url(r'^post/create/$', views.post_create_view, name='post_create'),
    url(r'^post/edit/(?P<id>\d+)/$', views.post_edit_view, name='post_edit'),
]