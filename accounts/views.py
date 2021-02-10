from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group

# Create your views here.
@login_required(login_url='auth_login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    pending_orders = orders.filter(status='Pending').count()
    out_for_delivery = orders.filter(status='Out for delivery').count()
    delivered_orders = orders.filter(status='Delivered').count()
    response = {'orders': orders, 'customers':customers, 'total_customers':total_customers, 'pending_orders':pending_orders, 'delivered_orders':delivered_orders, 'total_orders':total_orders, 'out_for_delivery':out_for_delivery}
    return render(request, 'accounts/dashboard.html', response)

@login_required(login_url='auth_login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='auth_login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk_text):
    customer = Customer.objects.get(id=pk_text)
    orders = customer.order_set.all()
    order_count = orders.count()

    query_filter = OrderFilter(request.GET, queryset=orders)
    orders = query_filter.qs
    return render(request, 'accounts/customers.html', {'customer':customer, 'orders':orders, 'order_count': order_count, 'query_filter':query_filter})

@login_required(login_url='auth_login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    order_form_set = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=8)
    customer = Customer.objects.get(id=pk)
    form_set = order_form_set(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        formset = order_form_set(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': form_set}
    return render(request, 'accounts/order_create.html', context)

@login_required(login_url='auth_login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    form = OrderForm(instance=order)
    context = {'form': form}
    return render(request, 'accounts/update_order_form.html', context)

@login_required(login_url='auth_login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if(request.method == 'POST'):
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)

@unauthenticated_user
def loginPage(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Invalid email or password')
            return render(request, 'accounts/login.html', context)
    return render(request, 'accounts/login.html', context)

def userPage(request):
    context = {}
    return render(request, 'accounts/user_page.html', context)

@login_required(login_url='auth_login')
def logoutPage(request):
    logout(request)
    context = {}
    return render(request, 'accounts/login.html', context)

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    context = {'form':form}
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account has been created successfully for ' + username)
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            return redirect('auth_login')
            
    return render(request, 'accounts/register.html', context)