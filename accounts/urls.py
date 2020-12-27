from django.urls import path
from .views import (home, customers, products, createOrder, updateOrder, deleteOrder)

urlpatterns = [
    path('', home, name='dashboard'),
    path('customer/<str:pk_text>', customers),
    path('products/', products, name='products'),
    path('orders/create/', createOrder, name='order_create'),
    path('update/order/<int:pk>', updateOrder, name='order_update'),
    path('delete/<int:pk>/order', deleteOrder, name='order_delete'),
]
