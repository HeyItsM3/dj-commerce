from django.shortcuts import render, redirect 
from django.http import JsonResponse
from django.db.models import Q
from .models import *
from .forms import *
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
import datetime



def searchProduct(request):
	data = cartData(request)

	cartItems = data['cartItems']

	searchP = request.GET.get("search")

	products = Product.objects.all()

	if searchP:
		products = Product.objects.filter(
			Q(name__icontains = searchP) 
		).distinct()

	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def registerPage(request):
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')

		context = {'form':form}
		return render(request, 'store/register.html', context)

def loginPage(request):
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('search')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'store/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def new_product(request):
	data = cartData(request)

	cartItems = data['cartItems']

	context = {'cartItems':cartItems}
	return render(request, 'store/new_product.html', context)

def contact(request):
	data = cartData(request)

	cartItems = data['cartItems']

	context = {'cartItems':cartItems }
	return render(request, 'store/contact.html', context)

def categories(request):
	data = cartData(request)

	cartItems = data['cartItems']

	products = Product.objects.all()[:6]
	context = {'products':products,'cartItems':cartItems}
	return render(request, 'store/categories.html', context)

def about(request):
	data = cartData(request)

	cartItems = data['cartItems']

	context = {'cartItems':cartItems}
	return render(request, 'store/about.html', context)

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()[:3]
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Se agrego un producto', safe=False)



def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)
	return JsonResponse('Pago realizado', safe=False)