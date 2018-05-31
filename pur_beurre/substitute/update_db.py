import requests as req

from .models import Product, Favorite
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

URL = 'https://world.openfoodfacts.org/language/french/'

def update_product(product_origin, product_updated):
    """Replace all attributes of the object in the database by the attributes of the object build from OPC"""
    for key in product_origin.__dict__:
        if key == 'id':
            #Don't wanna change id
            continue
        else:
            product_origin.__dict__[key] = product_updated.__dict__[key]
    return product_origin

def update_db():
    """Function use to ger all french products in the openfoodfacts database"""
    last_page = False
    i = 1
    while not last_page:
        url = URL + str(i) +'.json'
        data = req.get(url)
        data = data.json()
        if data['products'] == []: #For an Heroku deployment, change this line by 'if i == 1   800:' else, 'if data['products'] == []:'
            last_page = True
        else:
            for product in data['products']:
                try:
                    name = product['product_name']
                    image = product['image_url']
                    categories = product['categories']
                    score = product['nutrition_grades']
                    code = product['code']
                    image_small_url = product['image_small_url']
                    nutriments = str(product['nutriments'])

                    if categories == "" or name == "" or score == "" or image == "" or code == "" or image_small_url == "" or nutriments == "" or len(nutriments) > 1500:
                        continue
                    else:
                        product_to_save = Product(name=name, image_url=image, categories=categories, score=score, code=code, image_small_url=image_small_url, nutriments=nutriments)

                        try:
                            product_to_update = Product.objects.get(code=product_to_save.code)
                            product_to_update = update_product(product_to_update, product_to_save)
                            product_to_update.save()
                            # print('Produit mis à jour')


                        except ObjectDoesNotExist:
                        	product_to_save.save()
                        	# print('Produit enregistré')

                        except MultipleObjectsReturned:
                            #Use to avoid problem of multiple product whith identical code
                            continue

                except KeyError:
                    continue
            i = i+1
    print('Mise à jour de la base terminée ! ')


if __name__ == "__main__":
	update_db()

