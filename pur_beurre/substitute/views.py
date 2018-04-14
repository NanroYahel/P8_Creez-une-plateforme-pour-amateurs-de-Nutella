from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import LoginForm, SignInForm
from .models import Product
from substitute import utils

def index(request):
	return render(request, 'substitute/index.html')

def legal(request):
	return render(request, 'substitute/legal.html')

def user_login(request):
	error = False

	if request.method == "POST":
		form = LoginForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)

			if user:
				login(request, user)
			else:
				error = True
	else:
		form = LoginForm()

	return render(request, 'substitute/login.html', locals())


def user_logout(request):
	logout(request)
	return redirect(reverse(index))

def sign_in(request):
	error = False

	if request.method == "POST":
		form = SignInForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			confirm_password = form.cleaned_data['confirm_password']

			if password != confirm_password:
				error = "Les deux mots de passe ne sont pas identiques ! "
			else:
				user = User.objects.create_user(username, email, password)
				user.save()
				confirmation_message = 'Le compte a bien été créé. Merci pour votre inscription !'
	else:
		form = SignInForm()

	return render(request, 'substitute/sign_in.html', locals())


def user_account(request):

	return render(request, 'substitute/account.html', locals())

def product_sheet(request, product_id):
	product_to_display = Product.objects.get(pk=product_id)
	return render(request, 'substitute/product_sheet.html', locals())
	
def search(request):
	query = request.GET.get('query')
	no_result_message = False
	no_query_message = False
	if not query:
		products = Product.objects.all()
		query = "" #Use to not display 'None' in the title of the result page
		no_query_message = True
	else:
		products = Product.objects.filter(name__icontains=query)

		if len(products) ==0:
			no_result_message = 'Sorry, there is no result...'	
	context = {
		'products':products,
		'keyword':query,
		'no_result_message':no_result_message,
		'no_query_message':no_query_message
	}

	return render(request, 'substitute/search_result.html', context)

def find_substitute(request, product_id):
	substitute_query = utils.find_substitute(product_id)
	list_substitute = []
	#Create a list of product object to display in the template
	for product in substitute_query:
		list_substitute.append(Product.objects.get(pk=product.id))
	return render(request, 'substitute/substitutes_found.html', locals())
