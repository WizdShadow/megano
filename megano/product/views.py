from django.shortcuts import render
from django.db.models import Max
from django.http import JsonResponse
from django.http import HttpResponse
import json
from .models import Category, Product, SpecificationsProduct, ProductTask, Reviews, ProductImages, Tags, Timebasket, Timeuser, Basket

def categories(request):
    cat = Category.objects.all()
    categories = []
    for i in cat:
        categories.append({
            'id': i.id,
            'title': i.title,
            "image":{
                "src": "https://img.mvideo.ru/Pdb/400438595b.jpg",
                "alt": "Image alt string"
                },
            "subcategories":[{
                "id": i.id,
                "title": i.title,
                "image":{
                    "src": "https://img.mvideo.ru/Pdb/400438595b.jpg",
                    "alt": "Image alt string"
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
            "images": [{"src": "https://3dnews.ru/assets/external/illustrations/2014/04/14/818600/00_logo_big.jpg", "alt": "test" }],
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
            "images": [{"src": "https://3dnews.ru/assets/external/illustrations/2014/04/14/818600/00_logo_big.jpg", "alt": "test" } ],
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
            "images": [{"src": "https://3dnews.ru/assets/external/illustrations/2014/04/14/818600/00_logo_big.jpg", "alt": "test" } ],
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
            "images": [{"src": "https://3dnews.ru/assets/external/illustrations/2014/04/14/818600/00_logo_big.jpg", "alt": "test" } ],
            "tags": [tag.tags.name for tag in tags],
            "reviews": [{"author": v.author.username, "email": v.author.email, "text": v.text, "rate": v.rate, "date": v.date} for v in rev]

        }
    )
    return JsonResponse(response, safe=False)


def slayer(request):
    filt = int(request.GET.get("currentPage"))
    pr = Product.objects.filter(dateFrom__isnull = False)
    response = {
        "items":[
            {
            "id": pr[filt - 1].id,
            "price": pr[filt - 1].price,
            "salePrice": pr[filt - 1].sale_price,
            "dateFrom": pr[filt - 1].dateFrom,
            "dateTo": pr[filt - 1].dateTo,
            "title": pr[filt - 1].title,
            "images":[{"src": "https://3dnews.ru/assets/external/illustrations/2014/04/14/818600/00_logo_big.jpg", "alt": "test" }],
            }
        ],
        "currentPage": filt,
        "lastPage": len(pr)
    }
    return JsonResponse(response)

def basket(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if request.user.is_authenticated:
            pr = Product.objects.get(id=data.get("id"))
            add = Basket.objects.create(user_id=request.user, product=pr, count=data.get("count"))
            add.save()
            return JsonResponse({"status": True})
        
        num = request.sessiin.get("user_id")
        user = Timeuser.objects.get(user=num)
        pr = Product.objects.get(id=data.get("id"))
        add = Timebasket.objects.create(user_id=user, product=pr, count=data.get("count"))
        add.save()
        return JsonResponse({"status": True})
        
    elif request.method == "GET":
            response = []
            user = request.session.get("user_id")
            
            if user == None:
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
            
            elif request.user.is_authenticated:
                pr = Basket.objects.get(user_id = request.user)
                spisoc= [item.product.id for item in pr]
                tagss = ProductTask.objects.filter(product_id__in = spisoc)
                
                if len(pr) == 0:
                    return JsonResponse({"status": None})
                
                response = {
                        "id": pr.product.id,
                        "category": pr.product.category.id,
                        "price": round(float(pr.product.price), 2),
                        "count": pr.product.count,
                        "date": pr.product.date,
                        "title":pr.product.title,
                        "description": pr.product.description,
                        "freeDelivery": pr.product.freeDelivery,
                        "images": [{"src": "https://3dnews.ru/assets/external/illustrations/2014/04/14/818600/00_logo_big.jpg", "alt": "test" }],
                        "tags": [{"id": tag.tags.id, "name": tag.tags.name} for tag in tagss],
                        "reviews":5,
                        "rating": pr.rate
                        }
                return JsonResponse(response)
                
            pr = Timebasket.objects.filter(user_id = user)
            spisoc= [item.product.id for item in pr]
            tagss = ProductTask.objects.filter(product_id__in = spisoc)
            
            if len(pr) == 0:
                return JsonResponse({"status": None})
            
            response = {
                    "id": pr.product.id,
                    "category": pr.product.category.id,
                    "price": round(float(pr.product.price), 2),
                    "count": pr.product.count,
                    "date": pr.product.date,
                    "title":pr.product.title,
                    "description": pr.product.description,
                    "freeDelivery": pr.product.freeDelivery,
                    "images": [{"src": "https://3dnews.ru/assets/external/illustrations/2014/04/14/818600/00_logo_big.jpg", "alt": "test" }],
                    "tags": [{"id": tag.tags.id, "name": tag.tags.name} for tag in tagss],
                    "reviews":5,
                    "rating": pr.rate
                    }
            return JsonResponse(response)
                    
            

def get_rev(request, id):
    rev = Reviews.objects.get(id=id)
    response = {"author": rev.author.username,
                "email": rev.author.email,
                "text": rev.text,
                "rate": rev.rate,
                "date": rev.date}
    return JsonResponse(response)
    
def get_tags(request):
    tags = Tags.objects.all()

    tags = [{"id": v.id, "name": v.name} for v in tags]
    return JsonResponse(tags, safe=False)


