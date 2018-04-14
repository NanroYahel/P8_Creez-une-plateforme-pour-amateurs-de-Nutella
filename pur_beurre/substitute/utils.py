import json

import requests as req
import psycopg2

from .models import Product

URL = 'https://world.openfoodfacts.org/language/french/'

DB = psycopg2.connect("dbname='food_test_application' user='ronan'")
cur = DB.cursor()

def get_data_from_opc():
	"""Function use to ger all french products in the openfoodfacts database"""
	last_page = False
	i = 1
	while not last_page:
		url = URL +	str(i) +'.json'
		data = req.get(url)
		data = data.json()
		if data['products'] == []:
			last_page=True
		else:
			for product in data['products']:
				try:
					name = product['product_name']
					image = product['image_url']
					categories = product['categories']
					score = product['nutrition_grades']
					code = product['code']

					if categories == "" or name == "" or score == "" or image == "" or code == "":
						continue
					else:
						product_to_save = Product(name=name, image_url=image, categories=categories, score=score, code=code)
						cur.execute("""INSERT INTO substitute_product (name, image_url, categories, score, code) \
						VALUES (%s, %s, %s, %s, %s)""",(product_to_save.name, product_to_save.image_url, product_to_save.categories, product_to_save.score, product_to_save.code))
				except KeyError:
					continue

			i = i+1
		print(i)
		DB.commit()
	print('Remplissage de la base terminé ! ')


#----------------- TO DELETE-------------------------
# def display_product_terminal():
# 	"""TO DELETE -> use for creating find_substitue fonction"""
# 	search_product = input("Entrez l'id d'un produit : ")
# 	product = Product.objects.get(pk=search_product)
# 	list_categories = product.categories.split(',')
# 	print(product.name)
# 	print(list_categories)
# 	return product


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
				# print(categories[i])
				test_query = substitute.filter(categories__icontains=categories[i])
				# print("longueur querry set : " + str(len(test_query)))

				if len(test_query.filter(score__lt=score)) == 0: #Test if the query contains substitute with a better score
					is_empty = True
				else:
					substitute = test_query
		else:
			break


	substitute = substitute.filter(score__lt=score)[:5]
	# print('Résultat query_set : ', substitute)

	#Loop to display result in the terminal, need to be change for display on the web application
	# for i in range(0,5):
	# 	try:
	# 		print("------New product-------")
	# 		print("name : " + substitute[i].name)
	# 		print("categories : " + substitute[i].categories)
	# 		print("score : " + substitute[i].score)
	# 	except IndexError:
	# 		print("Il n'y en a pas plus...")
	# 		break


	# Loop for the final utilisation in the view
	list_substitute = []
	for substitute_product in substitute:
		list_substitute.append(substitute_product)

	return list_substitute

def test_function():
	search_product = input("Entrez l'id d'un produit : ")
	find_substitute(search_product)




