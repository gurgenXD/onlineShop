from django.urls import path
from shop import views


urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('<category_slug>/', views.category, name='category'),
    path('search/products/', views.search_products, name='search_products'),
    path('<category_slug>/<subcategory_slug>/', views.subcategory, name='subcategory'),
    path('<category_slug>/<subcategory_slug>/<product_slug>/', views.product, name='product'),
]
