from django.urls import path
from albums import views


urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('album/<album_id>/', views.album_detail, name='album_detail'),
]
