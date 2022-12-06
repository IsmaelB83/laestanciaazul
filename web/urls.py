# coding=utf-8
# Python imports
# Django imports
from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import handler404, handler500
# Third party app imports
# Local app imports
from . import views


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^', include(('post.urls', 'blog'), namespace='blog')),
    re_path(r'^user/', include(('user.urls', 'user'), namespace='user')),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
]

handler404 = views.error_404
handler500 = views.error_500

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
