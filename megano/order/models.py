from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class OrderModel(models.Model):
    createdAt= models.CharField(max_length=100, null=True, blank=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    deliveryType = models.CharField(max_length=100, null=True, blank=True)
    paymentType = models.CharField(max_length=100, null=True, blank=True)  
    totalCost = models.IntegerField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

class OrderProdcut(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()