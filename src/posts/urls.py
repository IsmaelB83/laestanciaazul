from django.conf.urls import url, include

from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout


from . import views
from .views import DeleteSocialProfileView, SelectAuthView, SocialProfileView, SocialProfileEditView

urlpatterns = [
    url(r'^$', views.index, name='index'), url(r'^contact/$', views.contact, name='contact'), url(r'^archive/$', views.archive, name='archive'),
    url(r'^category/(?P<id>all|prog|rpi|linux|sap|other)/$', views.category, name='category'),
    url(r'^post/(?P<id>\d+)/$', views.post_view, name='post'), url(r'^post/create/$', views.post_create, name='post_create'),
    url(r'^post/edit/(?P<id>\d+)/$', views.post_edit, name='post_edit'),
    url(r'^profile/(?P<id>\d+)/$', views.profile, name='profile'),

    # Profile Self View
    url(r'^sp$', never_cache(SocialProfileView.as_view()), name="sp_profile_view_page"), # Profile Other View
    url(r'^spview/(?P<username>\w+)/$', SocialProfileView.as_view(), name="sp_profile_other_view_page"), # Profile Edit
    url(r'^spedit/$', never_cache(login_required(SocialProfileEditView.as_view())), name="sp_profile_edit_page"), # Select Sign Up Method
    url(r'^spselect/$', never_cache(SelectAuthView.as_view()), name="sp_select_page"), # Delete
    url(r'^spdelete/$', login_required(DeleteSocialProfileView.as_view()), name="sp_delete_page"),
]

#   url(r'^post/(?P<id>\d+)/$', views.posts_detail, name='detail'),
#   url(r'^list/$', views.posts_list, name='list'),
#   url(r'^(?P<id>\d+)/edit/$', views.posts_update, name='update'),
#   url(r'^(?P<id>\d+)/delete/$', views.posts_delete, name='delete'),
