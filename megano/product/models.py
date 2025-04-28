from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=100)
    images = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.CharField(max_length=100)
    count = models.IntegerField()
    title = models.CharField(max_length=100, default="No title")
    description = models.TextField()
    fullDescription = models.TextField(default="No fullDescription")
    freeDelivery = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=10, decimal_places=1)

    def __str__(self):
        return self.title


class ProductImages(models.Model):
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.CharField(max_length=100)

    
class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class ProductTask(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE)

class Reviews(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default="No text")
    rate  = models.IntegerField()
    date = models.CharField(max_length=100)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

class Specifications(models.Model):
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class SpecificationsProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specific = models.ForeignKey(Specifications, on_delete=models.CASCADE)
