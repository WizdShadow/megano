from django.db.models import Max
from .models import Basket, Product, Timebasket, Timeuser, ProductTask, ProductImages


def post_basket(request, data):
    st = Basket.objects.filter(user_id = request.user, product_id = data.get("id"))  
    if st:
        st[0].count += data.get("count")
        st[0].save()
        return 
            
    pr = Product.objects.get(id=data.get("id"))
    add = Basket.objects.create(user_id=request.user, product=pr, count=data.get("count"))
    add.save()
    return


def post_basket_notuser(request, data):
    num = request.session.get("user_id")
    user = Timeuser.objects.get(user=num)
        
    st = Timebasket.objects.filter(user_id = user, product_id = data.get("id"))
    if st: 
            
        st[0].count += data.get("count")
        st[0].save()
        return 
    pr = Product.objects.get(id=data.get("id"))
    add = Timebasket.objects.create(user_id=user, product=pr, count=data.get("count"))
    add.save()
    return  


def get_basket(request):
    response = []

    pr = Basket.objects.filter(user_id = request.user)
    for v in pr:
        response.append({
            "id": v.product.id,
            "category": v.product.category.id,
            "price": round(float(v.product.price), 2),
            "count": v.count,
            "date": v.product.date,
            "title":v.product.title,
            "description": v.product.description,
            "freeDelivery": v.product.freeDelivery,
            "images": [{"src": val.image, "alt": val.image } for val in ProductImages.objects.filter(id_product_id=v.product)],
            "tags": [tag.tags.name for tag in ProductTask.objects.filter(product=v.product)],
            "reviews": 5,
            "rating": round(float(v.product.rating), 1),
        })

    return response


def get_basket_notuser(request):
    response = []

    pr = Timebasket.objects.filter(user_id = request.session.get("user_id"))
    for v in pr:
        response.append({
            "id": v.product.id,
            "category": v.product.category.id,
            "price": round(float(v.product.price), 2),
            "count": v.count,
            "date": v.product.date,
            "title":v.product.title,
            "description": v.product.description,
            "freeDelivery": v.product.freeDelivery,
            "images": [{"src": val.image, "alt": val.image } for val in ProductImages.objects.filter(id_product_id=v.product)],
            "tags": [tag.tags.name for tag in ProductTask.objects.filter(product=v.product)],
            "reviews": 5,
            "rating": round(float(v.product.rating), 1),
        })

    return response


def get_basket_create(request):
    num = Timeuser.objects.aggregate(max_num = Max("user"))
                
    if num.get("max_num") == None:
        request.session["user_id"] = 1
        add = Timeuser.objects.create(user=1)
        add.save()
        return 
                
    request.session["user_id"] = num.get("max_num") + 1
    request.session["order_id"] = []
    add = Timeuser.objects.create(user=num.get("max_num")+1)
    add.save()
    return


def delete_basket(request, data): 
    st = Basket.objects.filter(user_id = request.user, product_id = data.get("id"))
    if st:
        if st[0].count == data.get("count"):
            st[0].delete()
            return 
        st[0].count -= int(data.get("count"))
        st[0].save()
        return


def delete_basket_notuser(request, data):
    user = request.session.get("user_id")
    pr = Timebasket.objects.filter(user_id = user, product_id = data.get("id"))
    if pr:
        if pr[0].count == data.get("count"):
            pr[0].delete()
            return 
        pr[0].count -= int(data.get("count"))
        pr[0].save()
        return
    

def get_catalog(name, minn, maxx, freeDelivery, available, category, sort, sortType, limit, tags):
    products = Product.objects.all()
    
    if name:
        products = products.filter(title__contains=name)
    if minn:
        products = products.filter(price__gte=minn)
    if maxx:
        products = products.filter(price__lte=maxx)
    if freeDelivery:
        if freeDelivery == "false":
            products = products.filter(freeDelivery=False)
        else:
            products = products.filter(freeDelivery=True)
    if available:
        products = products.filter(count__gt=0)
    if category:
        products = products.filter(category_id=category)
    if sort:
        if sortType == "inc":
            products = products.order_by(sort)
        elif sortType == "dec":
            products = products.order_by("-"+sort)
    if limit:
        products = products[:int(limit)]
    if tags:
        products = products.filter(tags__id__in=tags)
    
    return products