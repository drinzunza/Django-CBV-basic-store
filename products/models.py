from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/categories/', null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products/', null=True, blank=True)
    liked_by = models.ManyToManyField(get_user_model(), related_name='liked_products', blank=True)


    def __str__(self):
        return self.name
