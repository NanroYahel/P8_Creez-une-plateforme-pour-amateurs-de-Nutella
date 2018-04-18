from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.URLField()
    categories = models.CharField(max_length=500)
    score = models.CharField(max_length=5)
    code = models.CharField(max_length=30)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
