from django.urls import path
from articles import views


urlpatterns = [
    path('', views.articles, name='articles'),
    path('<article_id>/', views.article_detail, name='article_detail'),
]
