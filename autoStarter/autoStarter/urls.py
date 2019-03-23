from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from filebrowser.sites import site


admin.site.site_header = 'Администрирование Avtostarter' 


urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('imagefit/', include('imagefit.urls')),
    path('tinymce/', include('tinymce.urls')),

    path('', include('landing.urls')),
    path('news/', include('news.urls')),
    path('catalog/', include('shop.urls')),
    path('accounts/', include('profiles.urls')),
    path('contacts/', include('contacts.urls')),
    path('orders/', include('orders.urls')),
    path('callback/', include('callback.urls')),
    path('gallery/', include('albums.urls')),
    path('articles/', include('articles.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
