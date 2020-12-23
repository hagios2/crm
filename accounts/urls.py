from django.urls import path
from .views import (home, customers, products)

urlpatterns = [
    path('dashboard/', home),
    path('customer/<str:pk_text>', customers),
    path('products/', products),


]
