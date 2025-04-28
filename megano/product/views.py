from django.shortcuts import render
from django.http import JsonResponse
from .models import Category

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