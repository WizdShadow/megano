from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Category, Product, SpecificationsProduct, ProductTask, Reviews, ProductImages, Tags

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


