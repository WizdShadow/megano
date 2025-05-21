from django.shortcuts import render
from django.db.models import Max
from django.http import JsonResponse
from django.http import HttpResponse
import json
from .models import Category, Product, SpecificationsProduct, ProductTask, Reviews, ProductImages, Tags, Timebasket, Timeuser, Basket

def categories(request):
    if request.method == 'GET':
        cat = Category.objects.all()
        categories = []
        for i in cat:
            categories.append({
                'id': i.id,
                'title': i.title,
                "image":{
                    "src": i.images,
                    "alt": i.images,
                    },
                "subcategories":[{
                    "id": i.id,
                    "title": i.title,
                    "image":{
                        "src": i.images,
                        "alt": i.images,
                        }
                }]
                }
            )
        return JsonResponse(categories, safe=False)

def product(request, id):
    if request.method == 'GET':
        pr = Product.objects.get(id=id)
        img = ProductImages.objects.filter(id_product_id=pr)
        tags = ProductTask.objects.filter(product=pr)
        rev = Reviews.objects.filter(product_id_id=pr)
        sef = SpecificationsProduct.objects.filter(product_id=pr)

        response = {
            "id": pr.id,
            "category": pr.category.id,
            "price": round(float(pr.price), 2),
            "count": pr.count,
            "date": pr.date,
            "title":pr.title,
            "description": pr.description,
            "fullDescription": pr.fullDescription,
            "freeDelivery": pr.freeDelivery,
            "images": [{"src": val.image, "alt": val.image } for val in img],
            "tags": [tag.tags.name for tag in tags],
            "reviews": [{"author": v.author.username, "email": v.author.email, "text": v.text, "rate": v.rate, "date": v.date} for v in rev],
            "specifications": [{"name": v.specific.name, "value": v.specific.value} for v in sef],
            "rating": round(float(pr.rating), 1),
        }
        return JsonResponse(response)
    

def popular(request):
    response = []
    pr = Product.objects.all()
    
    for v in pr:
        img = ProductImages.objects.filter(id_product_id=v)
        tags = ProductTask.objects.filter(product=v)
        rev = Reviews.objects.filter(product_id_id=v)
        response.append({
            "id": v.id,
            "category": v.category.id,
            "price": round(float(v.price), 2),
            "count": v.count,
            "date": v.date,
            "title":v.title,
            "description": v.description,
            "fullDescription": v.fullDescription,
            "freeDelivery": v.freeDelivery,
            "images": [{"src": val.image, "alt": val.image } for val in img],
            "tags": [tag.tags.name for tag in tags],
            "reviews": [{"author": v.author.username, "email": v.author.email, "text": v.text, "rate": v.rate, "date": v.date} for v in rev]

        }
    )
    return JsonResponse(response, safe=False)


def banner(request):
    response = []
    pr = Product.objects.all()
    for v in pr:
        img = ProductImages.objects.filter(id_product_id=v)
        tags = ProductTask.objects.filter(product=v)
        rev = Reviews.objects.filter(product_id_id=v)
        response.append({
            "id": v.id,
            "category": v.category.id,
            "price": round(float(v.price), 2),
            "count": v.count,
            "date": v.date,
            "title":v.title,
            "description": v.description,
            "fullDescription": v.fullDescription,
            "freeDelivery": v.freeDelivery,
            "images": [{"src": val.image, "alt": val.image } for val in img],
            "tags": [tag.tags.name for tag in tags],
            "reviews": [{"author": v.author.username, "email": v.author.email, "text": v.text, "rate": v.rate, "date": v.date} for v in rev]

        }
    )
    return JsonResponse(response, safe=False)


def limitid(request):
    response = []
    pr = Product.objects.all()
    for v in pr:
        img = ProductImages.objects.filter(id_product_id=v)
        tags = ProductTask.objects.filter(product=v)
        rev = Reviews.objects.filter(product_id_id=v)
        response.append({
            "id": v.id,
            "category": v.category.id,
            "price": round(float(v.price), 2),
            "count": v.count,
            "date": v.date,
            "title":v.title,
            "description": v.description,
            "fullDescription": v.fullDescription,
            "freeDelivery": v.freeDelivery,
            "images": [{"src": val.image, "alt": val.image } for val in img],
            "tags": [tag.tags.name for tag in tags],
            "reviews": [{"author": v.author.username, "email": v.author.email, "text": v.text, "rate": v.rate, "date": v.date} for v in rev]

        }
    )
    return JsonResponse(response, safe=False)


def slayer(request):
    filt = int(request.GET.get("currentPage"))
    pr = Product.objects.filter(dateFrom__isnull = False)
    img = ProductImages.objects.filter(id_product_id=pr[filt - 1])
    response = {
        "items":[
            {
            "id": pr[filt - 1].id,
            "price": pr[filt - 1].price,
            "salePrice": pr[filt - 1].sale_price,
            "dateFrom": pr[filt - 1].dateFrom,
            "dateTo": pr[filt - 1].dateTo,
            "title": pr[filt - 1].title,
            "images":[{"src": val.image, "alt": val.image } for val in img],
            }
        ],
        "currentPage": filt,
        "lastPage": len(pr)
    }
    return JsonResponse(response)

def basket(request):
    data = []
    if request.method == "POST":
        data = json.loads(request.body)
        
        if request.user.is_authenticated:
            st = Basket.objects.filter(user_id = request.user, product_id = data.get("id"))
            
            if st:
                st[0].count += data.get("count")
                st[0].save()
                return JsonResponse({"status": True})
            
            pr = Product.objects.get(id=data.get("id"))
            add = Basket.objects.create(user_id=request.user, product=pr, count=data.get("count"))
            add.save()
            return JsonResponse({"status": True})
        
        num = request.session.get("user_id")
        user = Timeuser.objects.get(user=num)
        
        st = Timebasket.objects.filter(user_id = user, product_id = data.get("id"))
        if st:
            if st[0].count + data.get("count") > st.product.count:
                return JsonResponse({"status": False})
            
            st[0].count += data.get("count")
            st[0].save()
            return JsonResponse({"status": True})
        
        pr = Product.objects.get(id=data.get("id"))
        add = Timebasket.objects.create(user_id=user, product=pr, count=data.get("count"))
        add.save()
        return JsonResponse({"status": True})
        
    elif request.method == "GET":
            response = []
            user = request.session.get("user_id")
            
            if request.user.is_authenticated:
                pr = Basket.objects.filter(user_id = request.user)
                for v in pr:
                    tagss = ProductTask.objects.filter(product_id = v.product.id)
                    img = ProductImages.objects.filter(id_product_id=v.product)
                    response = {
                            "id": v.product.id,
                            "category": v.product.category.id,
                            "price": round(float(v.product.price), 2),
                            "count": v.count,
                            "date": v.product.date,
                            "title":v.product.title,
                            "description": v.product.description,
                            "freeDelivery": v.product.freeDelivery,
                            "images": [{"src": val.image, "alt": val.image } for val in img],
                            "tags": [{"id": val.tags.id, "name": val.tags.name} for val in tagss],
                            "reviews":5,
                            "rating": v.product.rating
                            }
                    data.append(response)
                return JsonResponse(data, safe=False)
            
            elif user == None:
                num = Timeuser.objects.aggregate(max_num = Max("user"))
                
                if num.get("max_num") == None:
                    request.session["user_id"] = 1
                    add = Timeuser.objects.create(user=1)
                    add.save()
                    return JsonResponse({"status": None})
                
                request.session["user_id"] = num.get("max_num") + 1
                add = Timeuser.objects.create(user=num.get("max_num")+1)
                add.save()
                return JsonResponse({"status": None})
                
            pr = Timebasket.objects.filter(user_id = user)
            
            if len(pr) == 0:
                return JsonResponse({"status": None})
            
            for v in pr:
                img = ProductImages.objects.filter(id_product_id=v.product)
                tagss = ProductTask.objects.filter(product_id = v.product.id)
                response = {
                        "id": v.product.id,
                        "category": v.product.category.id,
                        "price": round(float(v.product.price), 2),
                        "count": v.count,
                        "date": v.product.date,
                        "title":v.product.title,
                        "description": v.product.description,
                        "freeDelivery": v.product.freeDelivery,
                        "images": [{"src": val.image, "alt": val.image } for val in img],
                        "tags": [{"id": val.tags.id, "name": val.tags.name} for val in tagss],
                        "reviews":5,
                        "rating": v.product.rating
                        }
                data.append(response)
            return JsonResponse(data, safe=False)
                
    elif request.method == "DELETE":
        data = json.loads(request.body)
        if request.user.is_authenticated:
            st = Basket.objects.filter(user_id = request.user, product_id = data.get("id"))
            if st:
                if st[0].count == data.get("count"):
                    st[0].delete()
                    return JsonResponse({"status": True})
                st[0].count -= int(data.get("count"))
                st[0].save()
                return JsonResponse({"status": True})  
        
        user = request.session.get("user_id")
        pr = Timebasket.objects.filter(user_id = user, product_id = data.get("id"))
        if pr:
            if pr[0].count == data.get("count"):
                pr[0].delete()
                return JsonResponse({"status": True})
            pr[0].count -= int(data.get("count"))
            pr[0].save()
            return JsonResponse({"status": True})
            

def get_rev(request, id):
    if request.method == "GET":
        rev = Reviews.objects.get(id=id)
        response = {"author": rev.author.username,
                    "email": rev.author.email,
                    "text": rev.text,
                    "rate": rev.rate,
                    "date": rev.date}
        return JsonResponse(response)
    
def get_tags(request):
    if request.method == "GET":
        tags = Tags.objects.all()
        tags = [{"id": v.id, "name": v.name} for v in tags]
        return JsonResponse(tags, safe=False)

def catalog(request):
    name = request.GET.get("filter[name]", None) 
    minn = request.GET.get("filter[minPrice]", None)
    maxx = request.GET.get("filter[maxPrice]", None)
    freeDelivery = request.GET.get("filter[freeDelivery]", None)
    available = request.GET.get("ffilter[available]", None)
    currentPage = request.GET.get("currentPage", None)
    category = request.GET.get("category", None)
    sort = request.GET.get("sort", None)
    sortType = request.GET.get("sortType", None)
    limit = request.GET.get("limit", None)
    tags = request.GET.get("tags[]", None)
    
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
    
    data = []
    for v in products:
        img = ProductImages.objects.filter(id_product_id=v.id)
        tagss = ProductTask.objects.filter(product_id = v.id)
        response = {
                "id": v.id,
                "category": v.category.id,
                "price": round(float(v.price), 2),
                "count": v.count,
                "date": v.date,
                "title":v.title,
                "description": v.description,
                "freeDelivery": v.freeDelivery,
                "images": [{"src": val.image, "alt": val.image } for val in img],
                "tags": [{"id": val.tags.id, "name": val.tags.name} for val in tagss],
                "reviews":5,
                "rating": v.rating
                }
        data.append(response)
    dicts = {"items": data}
    return JsonResponse(dicts, safe=False)

