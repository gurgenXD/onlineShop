from django.urls import path
from orders import views


urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add, name='add'),
    path('cart/remove/', views.remove, name='remove'),
    path('cart/change_quantity/', views.change_quantity, name='change_quantity'),
    path('contact_info/', views.contact_info, name='contact_info'),
    path('order/', views.order, name='order'),
    path('order_one_click/', views.order_one_click, name='order_one_click'),
    path('order_submit/', views.order_submit, name='order_submit'),
]
