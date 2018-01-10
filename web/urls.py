# coding=utf-8
# Python imports
# Django imports
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import handler404, handler500
# Third party app imports
# Local app imports
from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("post.urls", namespace='blog')),
    url(r'^user/', include("user.urls", namespace='user')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]

handler404 = views.error_404
handler500 = views.error_500

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
