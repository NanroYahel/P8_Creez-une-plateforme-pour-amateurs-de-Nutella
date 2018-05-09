import json

from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse

from .forms import LoginForm, SignInForm
from .models import Product, Favorite
from substitute import utils

#Globales variables used for the pagination of search results
PRODUCTS_LIST = ''
USER_QUERY = ''

def index(request):
    """Display the main page of the application"""
    return render(request, 'substitute/index.html')

def legal(request):
    """Display legal notice"""
    return render(request, 'substitute/legal.html')

def user_login(request):
    """View used to login"""

    #Use to store the error message in case of error
    error = False

    #If POST request, try to connect the user
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
    #If not POST request display the form to login
    else:
        form = LoginForm()

    return render(request, 'substitute/login.html', locals())


def user_logout(request):
    """View used to logout the user"""
    logout(request)
    return redirect(reverse(index))

def sign_in(request):
    """View to sign-in"""

    #Use to store the error message in case of error
    error = False

    #If POST request, try to create a new user with the informations.
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
    #If not POST request, display the form
    else:
        form = SignInForm()

    return render(request, 'substitute/sign_in.html', locals())


def user_account(request):
    """Display the name and the email of the user"""
    return render(request, 'substitute/account.html', locals())

def product_sheet(request, product_id):
    """View to display the selected product"""
    product_to_display = Product.objects.get(pk=product_id)
    product_to_display.nutriments = json.loads(product_to_display.nutriments.replace('\'', '"'))
    score_image = 'substitute/img/nutriscore-' + product_to_display.score + '.svg'

    return render(request, 'substitute/product_sheet.html', locals())

def search(request):
    """View that manage the search function"""

    no_result_message = False
    no_query_message = False

    #Use global variables to store the query and the result of the search 
    #Those gobal variables are usefull because of the pagination
    global PRODUCTS_LIST
    global USER_QUERY

    if request.method == "POST":
        query = request.POST.get('query')

        if not query:
            #If the user don't write a product name, display all the products
            PRODUCTS_LIST = Product.objects.all().order_by('name')
            query = "" #Use to not display 'None' in the title of the result page
            no_query_message = True
        else:
            #Search products with an name containing the query
            PRODUCTS_LIST = Product.objects.filter(name__icontains=query).order_by('name')
            USER_QUERY = query

            if not PRODUCTS_LIST:
            #If no result, display all the products
                no_result_message = 'Sorry, there is no result...'
                PRODUCTS_LIST = Product.objects.all().order_by('name')


    paginator = Paginator(PRODUCTS_LIST, 30)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products':products,
        'query':USER_QUERY,
        'no_result_message':no_result_message,
        'no_query_message':no_query_message,
        'paginate':True
    }

    return render(request, 'substitute/search_result.html', context)

def find_substitute(request, product_id):
    """View that display the selected product and the substitutes associate"""
    product_selected = Product.objects.get(pk=product_id)
    score_image = 'substitute/img/nutriscore-' + product_selected.score + '.svg'
    substitute_query = utils.find_substitute(product_id)
    list_substitute = []
    #Create a list of product object to display in the template
    for product in substitute_query:
        list_substitute.append(Product.objects.get(pk=product.id))

    if list_substitute == []:
        no_substitute = "Sorry, there is no substitute for this product in our database... "

    return render(request, 'substitute/substitutes_found.html', locals())

@login_required
def add_favorite(request, product_id):
    """Add the product selected in the list of favorite of the user"""
    query = product_id
    result_message = ""
    if query:
        try:
            Favorite.objects.get(user_id=request.user.id, product_id=int(query))
            result_message = "Ce produit est déjà dans vos favoris."
        except ObjectDoesNotExist:
            new_favorite = Favorite.objects.create(user_id=request.user.id, product_id=int(query))
            new_favorite.save()
            result_message = "Le produit a bien été enregistré."

    # context = {
    #     'result_message': result_message
    # }
    return HttpResponse(result_message)

@login_required
def favorites(request):
    """View that display all the favorites of the user"""
    favorites_query = utils.find_favorites(request.user)
    favorites_list = []
    for favorite in favorites_query:
        favorites_list.append(Product.objects.get(pk=favorite.product.id))

    return render(request, 'substitute/favorites.html', locals())
