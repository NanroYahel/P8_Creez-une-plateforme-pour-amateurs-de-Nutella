"""Test module"""
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Product, Favorite
from . import utils

class UtilsTestCase(TestCase):
    """Class to test the functions of 'utils' module"""

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
