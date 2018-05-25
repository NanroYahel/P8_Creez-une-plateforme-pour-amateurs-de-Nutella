"""Models used for the application"""
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """Model use to stock products"""
    name = models.CharField(max_length=200)
    image_url = models.URLField()
    image_small_url = models.URLField()
    categories = models.CharField(max_length=500)
    score = models.CharField(max_length=5)
    nutriments = models.CharField(max_length=1500)
    code = models.CharField(max_length=30)

class Favorite(models.Model):
    """Model used to stock the favorites products of an user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
