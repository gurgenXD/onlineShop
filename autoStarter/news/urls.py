from django.urls import path
from news import views


urlpatterns = [
    path('', views.news, name='news'),
    path('<news_slug>/', views.news_detail, name='news_detail'),
]
