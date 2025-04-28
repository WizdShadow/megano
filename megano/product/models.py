from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)
    images = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    fullDescription = models.TextField()
    freeDelivery = models.BooleanField()
    
    

    def __str__(self):
        return self.name
    
class Tags(models.Model):
    name = models.CharField(max_length=100)
    
