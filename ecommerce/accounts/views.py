from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


#from django.contrib.auth.forms import UserCreationForm
#from django.user.auth import UserForm
#from .filter import OrderFilter
#from .filter import OrderFilter

# Create your views here.
def logOutPage(request):
    logout(request)
    return redirect('login')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            '''
            if user is not None:
                login(request, user)
                return redirect('home')
                '''
            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                messages.error(request, 'Username or password is incorrect')
                return render(request, 'accounts/login.html')


                ''''
        if user is not None:
            login(request, user)
            return redirect('home')
    '''
        return render(request, 'accounts/login.html')
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Form was created successfully for:' +user)
                return redirect('login')
        context = {'form': form}
        return render(request, 'accounts/register.html',context)
@login_required(login_url = 'login')
def home(request):

    customers = Customer.objects.all()
    orders = Order.objects.all()

    order_count = orders.count()
    #total_customers = Customer.objects.all().count()
    #total_orders = Order.objects.all().count()
    total_customers = customers.count()
    total_orders = orders.count()
    #order_count = orders.count()


    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    context ={
    'customers': customers,
    'orders': orders,
    'total_orders': total_orders,
    'delivered': delivered,
    'pending': pending,
    }

    return render(request, 'accounts/dashboard.html', context)
@login_required(login_url = 'login')
def products(request):
    products = Product.objects.all()
    context = {
    'products': products
    }


    return render(request, 'accounts/products.html', context)

@login_required(login_url = 'login')
def customer(request, pk_test):
    customer = Customer.objects.get(id = pk_test)
    orders = customer.order_set.all()

    order_count  = orders.count()

    #myFilter = OrderFilter(queryset = orders.GET, orders.count)
    myFilter = OrderFilter(request.GET, queryset = orders)
    orders = myFilter.qs


    context = {
    'customer': customer,
    'orders': orders,
    'order_count': order_count,
    'myFilter': myFilter,

    }

    return render(request, 'accounts/customer.html', context)

@login_required(login_url = 'login')
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product', 'status'), extra = 10)
    #object = Order.objects.get(id = pk)

    customer = Customer.objects.get(id = pk)

    #form  = OrderForm(initial = {'customer':customer})
    formset = OrderFormSet(queryset = Order.objects.none(), instance = customer)
    if request.method == 'POST':
        #form  = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance = customer)

        if formset.is_valid():
            formset.save()
            return redirect('/')


        #print('Sending request:', request.POST)
    context = {
    'formset': formset
    }
    return render(request, 'accounts/order_form.html', context)
@login_required(login_url = 'login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)

    formset = OrderForm(instance = order)
    context = {
    'formset': formset
    }
    if request.method == 'POST':
        form = OrderForm(request.POST, instance = order )
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/order_form.html', context)
@login_required(login_url = 'login')
def deleteOrder(request, pk):

    order = Order.objects.get(id=pk)
    context = {
    'item': order
    }
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    return render(request, 'accounts/delete_order.html', context)

'''
def createCustomer(request):
    customer = Customer.objects.all()
    name = customer.objects.get()
    context = {
    'name': name
    }

    return render(request, 'accounts/create_customer.html', name)
'''
