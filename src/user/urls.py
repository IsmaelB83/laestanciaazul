# Python imports
# Django imports
from django.conf.urls import url
# Third party app imports
# Local app imports
from . import views


urlpatterns = [
    url(r'^profile/(?P<id>\d+)/$', views.profile, name='profile'),
    url(r'^password/$', views.password, name='password'),
    url(r'^register/$', views.register, name='register'),
]
