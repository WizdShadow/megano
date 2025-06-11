import json
import time
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import HttpResponse


from order.func import get_orders, get_order_id
from product.models import Product
from .models import OrderProdcut, OrderModel


def order(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            summ = 0
            data = json.loads(request.body)
            user = User.objects.get(pk=request.user.pk)
            current_time = time.localtime()
            t = time.strftime("%d.%m.%Y %H:%M:%S", current_time)
            for val in data:
                summ += val.get("count") * val.get("price")
            new_order = OrderModel.objects.create(createdAt=t, totalCost=summ, fullname=user.username)
            new_order.save()
            for val in data:
                product = Product.objects.get(id=val.get("id"))
                add = OrderProdcut.objects.create(order=new_order, count=val.get("count"), product=product)
                add.save
                return JsonResponse({"orderId": new_order.id})
            else:
                data = json.loads(request.body)
                current_time = time.localtime()
                t = time.strftime("%d.%m.%Y %H:%M:%S", current_time)
                user = request.session.get("user_id")
                new_order = OrderModel.objects.create(createdAt=t)
                new_order.save()
                request.session["order_id"].append(new_order.id)
                for i in data:
                    product = Product.objects.get(id=i.get("id"))
                    add = OrderProdcut.objects.create(order=new_order, count=i.get("count"), product=product)
                    add.save
                return JsonResponse({"orderId": new_order.id})
    elif request.method == "GET":
        if request.user.is_authenticated:
            ords = get_orders(request)
            return JsonResponse(ords, safe=False)


def order_id(request, id):
    if request.method == "GET":
        order = OrderModel.objects.get(pk=id)
        spisoc = get_order_id(request, id)
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
        return JsonResponse({"orderId": order.id})


def payment(request, id):
    if request.method == "POST":
        order = OrderModel.objects.get(pk=id)
        order.status = "paid"
        order.save()
        return HttpResponse(status=200)
