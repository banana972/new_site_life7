from django.shortcuts import render, redirect
from django.forms import inlineformset_factory 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from . import models
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


def func():
	print('Worked')
function = func

@unauthenticated_user
def register_page(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			
			messages.success(request, 'Account has been created for ' + username)
			return redirect('login-url')
			
	context = {'form': form, 'function': function}
	return render(request, 'accounts/register.html', context)

@login_required(login_url = 'login-url')
@allowed_users(allowed_roles = ['customer'])
def user_page(request):
	orders = request.user.customer.order_set.all()
	
	total_orders = orders.count()
	delivered = orders.filter(status = 'Delivered').count()
	pending = orders.filter(status = 'Pending').count()
	print('orders' + str(orders))
	
	context = {
		'orders': orders,
		'total_orders': total_orders,
		'delivered': delivered,
		'pending': pending
	}
	return render(request, 'accounts/user.html', context)

	
@unauthenticated_user
def login_page(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(request, username = username, password = password)
		
		if user is not None:
			login(request, user)
			return redirect('dashboard-url')			
		else:
			messages.info(request, 'Username OR password is incorrect')
			
	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login-url')	

@login_required(login_url = 'login-url')
@admin_only
def dashboard(request):
	orders = models.Order.objects.all() 
	customers = models.Customer.objects.all()
	
	total_customers = customers.count()
	
	total_orders = orders.count()
	delivered = orders.filter(status = 'Delivered').count()
	pending = orders.filter(status = 'Pending').count()

	
	context = {
		'orders': orders,
		'customers': customers,
		'total_customers': total_customers,
		'total_orders': total_orders,
		'delivered': delivered,
		'pending': pending
	}
	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url = 'login-url')
@allowed_users(allowed_roles = ['admin'])
def products(request):
	products = models.Product.objects.all()
	
	context =  {'products': products}
	
	return render(request, 'accounts/products.html', context)

@login_required(login_url = 'login-url')	
@allowed_users(allowed_roles = ['admin'])
def customer(request, pk):
	customer = models.Customer.objects.get(id = pk)
	
	orders = customer.order_set.all()
	order_counts = orders.count()
	
	myFilter = OrderFilter(request.GET, queryset = orders)
	orders = myFilter.qs
	
	context = {
		'customer': customer,
		'orders': orders,
		'order_counts': order_counts,
		'myFilter': myFilter
	}
	return render(request, 'accounts/customer.html', context)


@login_required(login_url = 'login-url')	
@allowed_users(allowed_roles = ['admin'])
def create_order(request, pk):
	OrderFormSet = inlineformset_factory(models.Customer, models.Order, fields = ('product','status'), extra = 10)	
	customer = models.Customer.objects.get(id = pk)
	formset = OrderFormSet(queryset = models.Order.objects.none(), instance = customer)
	#form = OrderForm(initial = {'customer': customer})	
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance = customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	
	context = {'formset': formset}
	return render(request, 'accounts/order_form.html', context)
	
	
@login_required(login_url = 'login-url')
@allowed_users(allowed_roles = ['admin'])
def update_order(request, pk):
	order = models.Order.objects.get(id = pk)
	form = OrderForm(instance = order)
	
	if request.method == 'POST':
		form = OrderForm(request.POST, instance = order)
		if form.is_valid():
			form.save()
			return redirect('/')
	
	context = {'formset': form}
	return render(request, 'accounts/order_form.html', context)
	
	
@login_required(login_url = 'login-url')	
@allowed_users(allowed_roles = ['admin'])
def delete_order(request, pk):
	order = models.Order.objects.get(id = pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	
	context = {'order': order}
	return render(request, 'accounts/delete.html', context)
	
@login_required(login_url = 'login-url')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance = customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance = customer)
		if form.is_valid():
			form.save()


	context = {'form': form}
	return render(request, 'accounts/account_settings.html', context)
	
	