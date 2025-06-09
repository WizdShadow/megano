from django.contrib.auth.models import User
from .models import OrderModel, OrderProdcut
from product.models import ProductTask, ProductImages, Reviews


def get_orders(request):
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

    return ords


def get_order_id(request, id):
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
    return spisoc