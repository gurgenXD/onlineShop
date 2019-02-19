from django.urls import path
from callback import views


urlpatterns = [
    path('', views.callback, name='callback'),
]
