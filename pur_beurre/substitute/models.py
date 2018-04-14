from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.URLField()
    categories = models.CharField(max_length=500)
    score = models.CharField(max_length=5)
    code = models.CharField(max_length=30)

