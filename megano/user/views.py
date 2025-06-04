from django.shortcuts import render
from django.shortcuts import redirect
from django.http import FileResponse,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import User, MyUser
from product.models import Product
from order.models import OrderProdcut, OrderModel
import json


def logins(request):
    if request.method != 'POST':
        return redirect('/')
    data = json.loads(request.body)
    user = User.objects.get(username=data.get('username'))
    
    
    if not user:
        return redirect('/login')
    
    if user.check_password(data.get('password')):
        user = authenticate(request, username=user.username, password=data.get('password'))
        login(request, user)
        return HttpResponse(status=200)
    
    return HttpResponse(status=200)   


def register(request):
    if request.method != 'POST':
        return redirect('/')
    data = json.loads(request.body)
    user = User.objects.create_user(
        username=data.get('username'),
        password=data.get('password'),
    )
    
    user.save()

    return HttpResponse(status=200)


@login_required
def logoutt(request):
    logout(request)
    return redirect('/')


@login_required
def profile(request):
    if request.method == 'GET':
        user = User.objects.get(pk=request.user.pk)
        response = {
            "fullName": user.username,
            "email": user.email,
            "phone": user.myuser.phone,
            "avatar": {
                "src": user.myuser.avatar,
                "alt": "Image alt string"
            }
        }
        return JsonResponse(response)
    user = User.objects.get(pk=request.user.pk)
    data = json.loads(request.body)
    user.username = data.get('fullName')
    user.email = data.get('email')
    user.myuser.phone = data.get('phone')
    user.save()
    return redirect('profile/')


@login_required
def post_profile_password(request):
    data = json.loads(request.body)
    user = User.objects.get(pk=request.user.pk)
    
    if user.check_password(data.get('password')):
        user.set_password(data.get('newPassword'))
        user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@login_required
def post_profile_avatar(request):
    file = request.FILES.get('avatar')
    user = User.objects.get(pk=request.user.pk)
    user.myuser.avatar = file
    user.myuser.save()
    with open(f"user/media/{user.pk}_{file}", "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)
    return JsonResponse({'status': 'success'})
    

@login_required
def get_images(request, filename):
    user = User.objects.get(pk=request.user.pk)
    if not user.myuser.avatar:
        return JsonResponse({'status': 'error'})
    path = f"user/media/{user.pk}_{user.myuser.avatar}"
    return FileResponse(open(path, 'rb'))