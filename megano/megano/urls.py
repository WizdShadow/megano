from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from user.views import get_images

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("frontend.urls")),
    path("api/", include("user.urls")),
    path("api/", include("product.urls")),
    path ('profile/<str:filename>', get_images, name='filename'),
    path("api/", include("order.urls")),
]
