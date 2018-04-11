import requests as req
import json

def get_data_from_openfoodfacts(url):
	data = req.get(url)
	data = data.json()
	name = data['product']['generic_name']
	image = data['product']['image_url']
	categories = data['product']['categories']
	score = data['product']['nutrition_grades']
	# score_image = data['product'][]
	return name, image, categories, score

#URL à utiliser pour les produits français : https://world.openfoodfacts.org/language/french/1.json
