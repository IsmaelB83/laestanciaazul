# coding=utf-8
# Python imports
# Django imports
from django.conf.urls import url
# Third party app imports
# Local app imports
from . import views


urlpatterns = [
    url(r'^bodypart/(?P<id>[\w]+)/$', views.bodypart_view, name='bodypart'),
	url(r'^exercise/(?P<id>[\w]+)/$', views.exercise_view, name='exercise'),
	url(r'^routine/(?P<id>[\w]+)/$', views.routine_view, name='routine'),
]