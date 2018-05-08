"""Module that contains all functions used in the application"""
import requests as req
import psycopg2

from .models import Product, Favorite

URL = 'https://world.openfoodfacts.org/language/french/'


########################### Function to fill the database with openfoodfacts (uncomment to use it) ###################
# # DB = psycopg2.connect("dbname='db_purbeurre' user='ronan'") #Usefull for a local use of the database
# cur = DB.cursor()

# def get_data_from_opc():
#     """Function use to ger all french products in the openfoodfacts database"""
#     last_page = False
#     i = 1
#     while not last_page:
#         url = URL + str(i) +'.json'
#         data = req.get(url)
#         data = data.json()
#         if data['products'] == []: #For an Heroku deployment, change this line by 'if i == 1800:' else, 'if data['products'] == []:'
#             last_page = True
#         else:
#             for product in data['products']:
#                 try:
#                     name = product['product_name']
#                     image = product['image_url']
#                     categories = product['categories']
#                     score = product['nutrition_grades']
#                     code = product['code']
#                     image_small_url = product['image_small_url']
#                     nutriments = str(product['nutriments'])

#                     if categories == "" or name == "" or score == "" or image == "" or code == "" or image_small_url == "" or nutriments == "" or len(nutriments) > 1500:
#                         continue
#                     else:
#                         product_to_save = Product(name=name, image_url=image, categories=categories, score=score, code=code, image_small_url=image_small_url, nutriments=nutriments)
#                         cur.execute("""INSERT INTO substitute_product (name, image_url, categories, score, code, image_small_url, nutriments) \
#                         VALUES (%s, %s, %s, %s, %s, %s, %s)""", (product_to_save.name, product_to_save.image_url, product_to_save.categories, product_to_save.score, product_to_save.code, product_to_save.image_small_url, product_to_save.nutriments))
#                 except KeyError:
#                     continue
#             #TO DELETE FOR DEF VERSION
#             DB.commit()
#             i = i+1
#         print(i)
#         # DB.commit() TO RETABLISH FOR DEF VERSION
#     print('Remplissage de la base terminé ! ')

######################################################################

def find_substitute(search_product):
    """Function matching a product with another product with better score and common categories"""
    product = Product.objects.get(pk=search_product)
    categories = product.categories.split(',')
    score = product.score

    is_empty = False

    substitute = Product.objects.filter(categories__icontains=categories[0])

    # Course all categories of the product, to find the products with the most categories in common
    for i in range(1, len(categories)):

        if not is_empty:
            test_query = substitute.filter(categories__icontains=categories[i])

            if score == 'a' and len(test_query.filter(score=score)) == 0:
                is_empty = True
            elif len(test_query.filter(score__lt=score)) == 0: #Test if the query contains substitute with a better score
                is_empty = True
            else:
                substitute = test_query
        else:
            break

    if score == 'a':
        substitute = substitute.filter(score=score)[:5]
    else:
        substitute = substitute.filter(score__lt=score)[:5]

    # Loop for the final utilisation in the view
    list_substitute = []
    for substitute_product in substitute:
        list_substitute.append(substitute_product)

    return list_substitute

def find_favorites(user):
    """Function matching a product with another product with better score and common categories"""
    list_favorites = Favorite.objects.all().filter(user_id=user.id)
    return list_favorites
