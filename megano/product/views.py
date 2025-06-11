import json
from django.http import JsonResponse
from .models import Category, Product, SpecificationsProduct, ProductTask, Reviews, ProductImages, Tags, Timebasket
from .func import post_basket_notuser, post_basket, get_basket, get_basket_create, get_basket_notuser, delete_basket, delete_basket_notuser, get_catalog


def categories(request):
    if request.method == 'GET':
        cat = Category.objects.all()
        categories = []
        for i in cat:
            categories.append({
                'id': i.id,
                'title': i.title,
                "image": {
                    "src": i.images,
                    "alt": i.images,
                    },
                "subcategories": [{
                    "id": i.id,
                    "title": i.title,
                    "image": {
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
            "title": pr.title,
            "description": pr.description,
            "fullDescription": pr.fullDescription,
            "freeDelivery": pr.freeDelivery,
            "images": [{"src": val.image, "alt": val.image} for val in img],
            "tags": [tag.tags.name for tag in tags],
            "reviews": [{"author": v.author.username,
                         "email": v.author.email,
                         "text": v.text,
                         "rate": v.rate,
                         "date": v.date} for v in rev],
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
            "title": v.title,
            "description": v.description,
            "fullDescription": v.fullDescription,
            "freeDelivery": v.freeDelivery,
            "images": [{"src": val.image, "alt": val.image} for val in img],
            "tags": [tag.tags.name for tag in tags],
            "reviews": [{"author": v.author.username,
                         "email": v.author.email,
                         "text": v.text,
                         "rate": v.rate,
                         "date": v.date} for v in rev]

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
            "title": v.title,
            "description": v.description,
            "fullDescription": v.fullDescription,
            "freeDelivery": v.freeDelivery,
            "images": [{"src": val.image, "alt": val.image} for val in img],
            "tags": [tag.tags.name for tag in tags],
            "reviews": [{"author": v.author.username,
                         "email": v.author.email, "text": v.text, "rate": v.rate, "date": v.date} for v in rev]

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
            "title": v.title,
            "description": v.description,
            "fullDescription": v.fullDescription,
            "freeDelivery": v.freeDelivery,
            "images": [{"src": val.image, "alt": val.image} for val in img],
            "tags": [tag.tags.name for tag in tags],
            "reviews": [{"author": v.author.username,
                         "email": v.author.email, "text": v.text, "rate": v.rate, "date": v.date} for v in rev]

            }
        )
    return JsonResponse(response, safe=False)


def slayer(request):
    filt = int(request.GET.get("currentPage"))
    pr = Product.objects.filter(dateFrom__isnull=False)
    img = ProductImages.objects.filter(id_product_id=pr[filt - 1])
    response = {
        "items": [
            {
                "id": pr[filt - 1].id,
                "price": pr[filt - 1].price,
                "salePrice": pr[filt - 1].sale_price,
                "dateFrom": pr[filt - 1].dateFrom,
                "dateTo": pr[filt - 1].dateTo,
                "title": pr[filt - 1].title,
                "images": [{"src": val.image, "alt": val.image} for val in img],
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
            post_basket(request, data)
            return JsonResponse({"status": True})
        post_basket_notuser(request, data)
        return JsonResponse({"status": True})
    elif request.method == "GET":
        user = request.session.get("user_id")
        if request.user.is_authenticated:
            data = get_basket(request)
            return JsonResponse(data, safe=False)
        elif user is None:
            get_basket_create(request)
            return JsonResponse({"status": None})
        pr = Timebasket.objects.filter(user_id=user)
        if len(pr) == 0:
            return JsonResponse({"status": None})
        data = get_basket_notuser(request)
        return JsonResponse(data, safe=False)
    elif request.method == "DELETE":
        data = json.loads(request.body)
        if request.user.is_authenticated:
            delete_basket(request, data)
            return JsonResponse({"status": True})
        delete_basket_notuser(request, data)
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
    products = get_catalog(name, minn, maxx, freeDelivery, available, category, sort, sortType, limit, tags)
    data = []
    for v in products:
        img = ProductImages.objects.filter(id_product_id=v.id)
        tagss = ProductTask.objects.filter(product_id=v.id)
        response = {
                "id": v.id,
                "category": v.category.id,
                "price": round(float(v.price), 2),
                "count": v.count,
                "date": v.date,
                "title": v.title,
                "description": v.description,
                "freeDelivery": v.freeDelivery,
                "images": [{"src": val.image, "alt": val.image} for val in img],
                "tags": [{"id": val.tags.id, "name": val.tags.name} for val in tagss],
                "reviews": 5,
                "rating": v.rating
                }
        data.append(response)
    dicts = {"items": data}
    return JsonResponse(dicts, safe=False)
