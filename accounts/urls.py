from django.urls import path
from .views import (home, customers, products, createOrder, updateOrder, deleteOrder, loginPage, register, logoutPage)

urlpatterns = [
    path('', home, name='dashboard'),
    path('customer/<int:pk_text>', customers, name='view_customer'),
    path('products/', products, name='products'),
    path('customer/<int:pk>/orders/create/', createOrder, name='order_create'),
    path('update/order/<int:pk>', updateOrder, name='order_update'),
    path('delete/<int:pk>/order', deleteOrder, name='order_delete'),
    path('auth/login', loginPage, name='auth_login'),
    path('auth/logout', logoutPage, name='auth_logout'),
    path('auth/register', register, name='auth_register')
]
