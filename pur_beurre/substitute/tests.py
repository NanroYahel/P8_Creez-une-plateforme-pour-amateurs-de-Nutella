"""Test module"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Product, Favorite
from . import utils



class IndexPageTestCase(TestCase):
    """Class to test the index view"""
    def test_index_page(self):
        """Test that index page return a 200 code"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class LegalPageTestCase(TestCase):
    """Class to test the legal view"""
    def test_legal_page(self):
        """Test that legal page return a 200 code"""
        response = self.client.get(reverse('substitute:legal'))
        self.assertEqual(response.status_code, 200)


class FunctionTestCase(TestCase):

    def setUp(self):
        """Create somme products in the database"""
        nutella = Product.objects.create(name='Nutella', score='e', categories='test', nutriments="{'test_nutriment': 10}")
        marmelade = Product.objects.create(name='Marmelade', score='d', categories='test', nutriments="{'test_nutriment': 10}")
        self.product_id = Product.objects.get(name='Nutella').id
        self.substitute_id = Product.objects.get(name='Marmelade').id

    def test_product_sheet_page(self):
        """Test that the product_sheet page return 200 code"""
        response = self.client.get(reverse('substitute:product_sheet', args=(self.product_id,)))
        self.assertEqual(response.status_code, 200)

    def test_find_substitute_page(self):
        """Test that the fiding substitute page return 200 code"""
        response = self.client.get(reverse('substitute:find_substitute', args=(self.product_id,)))
        self.assertEqual(response.status_code, 200)

    def test_user_account_page(self):
        """Test that the user account page return 200 code"""
        response = self.client.get(reverse('substitute:account',))
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        user_search = "nutel"
        response_no_query = self.client.get(reverse('substitute:search'))
        response_query = self.client.get(reverse('substitute:search', args=('query':user_search,)))
        self.assertEqual(response.status_code, 200)
        print(response)



class UtilsTestCase(TestCase):

    def setUp(self):
        """Create somme products in the database"""
        nutella = Product.objects.create(name='Nutella', score='e', categories='test', nutriments="{'test_nutriment': 10}")
        marmelade = Product.objects.create(name='Marmelade', score='d', categories='test', nutriments="{'test_nutriment': 10}")
        self.product_id = Product.objects.get(name='Nutella').id
        self.substitute_id = Product.objects.get(name='Marmelade').id
        user_with_favorite = User.objects.create(username='test_user')
        user_without_favorite = User.objects.create(username='no_favorite_user')
        self.user = User.objects.get(username='test_user')
        self.no_favorite_user = User.objects.get(username='no_favorite_user')
        favorite = Favorite.objects.create(user_id=self.user.id, product_id=self.substitute_id)
        

    def test_find_substitute(self):
        """Test that the finding substitute function return correctly substitutes"""
        has_substitute = utils.find_substitute(self.product_id)
        no_substitute = utils.find_substitute(self.substitute_id)
        self.assertEqual(len(has_substitute), 1)
        self.assertEqual(len(no_substitute), 0)

    def test_find_favorites(self):
        """Test the finding favorites function"""
        has_favorites = utils.find_favorites(self.user)
        no_favorite = utils.find_favorites(self.no_favorite_user)
        self.assertEqual(len(has_favorites), 1)
        self.assertEqual(len(no_favorite), 0)





