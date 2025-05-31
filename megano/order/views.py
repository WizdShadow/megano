from django.shortcuts import render
from django.db.models import Max
from django.http import JsonResponse
from django.contrib.auth.models import User
from product.models import Timeuser
from django.http import HttpResponse
import json
import time

from product.models import Product

from .models import OrderProdcut, OrderModel
from product.models import Product, ProductImages, ProductTask, Reviews

def order(request):
    if request.method == "POST":
            if request.user.is_authenticated:
                summ = 0
                data = json.loads(request.body)
                user = User.objects.get(pk=request.user.pk)
                current_time = time.localtime()
                t = time.strftime("%d.%m.%Y %H:%M:%S",current_time)
                for val in data:
                    summ += val.get("count") * val.get("price")
                new_order = OrderModel.objects.create(createdAt=t, totalCost=summ, fullname = user.username)
                new_order.save()
                for val in data:
                    product = Product.objects.get(id=val.get("id"))
                    add = OrderProdcut.objects.create(order=new_order, count=val.get("count"), product=product)
                    add.save
            
                return JsonResponse({"orderId": new_order.id})
            else:
                data = json.loads(request.body)
                current_time = time.localtime()
                t = time.strftime("%d.%m.%Y %H:%M:%S",current_time)
                user = request.session.get("user_id")
                user_orm = Timeuser.objects.get(user=user)
                new_order= OrderModel.objects.create(createdAt=t)
                new_order.save()
                request.session["order_id"].append(new_order.id)
                for i in data:
                    product = Product.objects.get(id=i.get("id"))
                    add = OrderProdcut.objects.create(order=new_order, count=i.get("count"), product=product)
                    add.save
                return JsonResponse({"orderId": new_order.id})
    
    
    elif request.method == "GET":
      if request.user.is_authenticated:
        ords = []
        user = User.objects.get(pk=request.user.pk)
        orders = OrderModel.objects.filter(fullname=user.username)
        for ord in orders:
            order = OrderProdcut.objects.filter(order=ord)
            products = []
            for o in order:
                products.append({
                    "id": o.product.id,
                    "category": o.product.category.id,
                    "price": o.product.price,
                    "count": o.count,
                    "date": o.product.date,
                    "title":o.product.title,
                    "description": o.product.description,
                    "freeDelivery": o.product.freeDelivery,
                    "images": [{"src": val.image, "alt": val.image } for val in ProductImages.objects.filter(id_product_id=o.product)],
                    "tags": [tag.tags.name for tag in ProductTask.objects.filter(product=o.product)],
                    "reviews": [{"author": v.author.username, "email": v.author.email, "text": v.text, "rate": v.rate, "date": v.date} for v in Reviews.objects.filter(product_id_id=o.product)],
                    "rating": round(float(o.product.rating), 1),
                })
            ords.append({"id": ord.id,
                         "createdAt": ord.createdAt,
                         "fullName": ord.fullname,
                         "email": ord.email,
                         "phone": ord.phone,
                         "deliveryType": ord.deliveryType,
                         "paymentType": ord.paymentType,
                         "totalCost": ord.totalCost,
                         "status": ord.status,
                         "city": ord.city,
                         "address": ord.address,
                         "products": products})
        return JsonResponse(ords, safe=False)
    
def order_id(request, id):
    if request.method == "GET":
        spisoc = []
        order = OrderModel.objects.get(pk=id)
        products = OrderProdcut.objects.filter(order=order)
        for pr in products:
            spisoc.append({
                "id": pr.product.id,
                "category": pr.product.category.id,
                "price": pr.product.price,
                "count": pr.count,
                "date": pr.product.date,
                "title":pr.product.title,
                "description": pr.product.description,
                "freeDelivery": pr.product.freeDelivery,
                "images": [{"src": val.image, "alt": val.image } for val in ProductImages.objects.filter(id_product_id=pr.product)],
                "tags": [tag.tags.name for tag in ProductTask.objects.filter(product=pr.product)],
                "reviews": 5,
                "rating": round(float(pr.product.rating), 1),
            })
        return JsonResponse({"id": order.id,
                             "createdAt": order.createdAt,
                             "fullName": order.fullname,
                             "email": order.email,
                             "phone": order.phone,
                             "deliveryType": order.deliveryType,
                             "paymentType": order.paymentType,
                             "totalCost": order.totalCost,
                             "status": order.status,
                             "city": order.city,
                             "address": order.address,
                             "products": spisoc})
    elif request.method == "POST":
        data = json.loads(request.body)
        order = OrderModel.objects.get(pk=id)
        order.phone = data.get('phone')
        order.email = data.get('email')
        order.deliveryType = data.get('deliveryType')
        order.city = data.get('city')
        order.address = data.get('address')
        order.paymentType = data.get('paymentType')
        order.status = data.get('status')
        order.save()
        return JsonResponse({"status": True})

def payment(request, id):
    if request.method == "POST":
        order = OrderModel.objects.get(pk=id)
        order.status = "paid"
        order.save()
        return HttpResponse(status=200)