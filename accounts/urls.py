from django.urls import path
from .views import (home, customers, products, createOrder)

urlpatterns = [
    path('dashboard/', home),
    path('customer/<str:pk_text>', customers),
    path('products/', products),
    path('orders/create/', createOrder, name='order_create'),

]
