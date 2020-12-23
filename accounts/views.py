from django.shortcuts import render
from .models import *
# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    pending_orders = orders.filter(status='Pending').count()
    delivered_orders = orders.filter(status='Delivered').count()
    response = {'orders': orders, 'customers':customers, 'total_customers':total_customers, 'pending_orders':pending_orders, 'delivered_orders':delivered_orders, 'total_orders':total_orders}
    return render(request, 'accounts/dashboard.html', response)


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customers(request, pk_text):
    customer = Customer.objects.get(id=pk_text)
    orders = customer.order_set.all()
    order_count = orders.count()
    return render(request, 'accounts/customers.html', {'customer':customer, 'orders':orders, 'order_count': order_count})

def createOrder(request):
    
    context = {}
    return render(request, 'accounts/order_create.html', context)