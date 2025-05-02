from django.urls import path
from .views import categories, product, get_tags, get_rev, popular, banner, limitid, slayer, basket

urlpatterns = [
    path('categories/', categories, name='categories'),
    path('product/<int:id>/', product, name='product'),
    path('tags/', get_tags, name='get_tags'),
    path('product/<int:id>/review', get_rev, name='get_rev'),
    path('products/popular/', popular, name='popular'),
    path('banners/', banner, name='banner'),
    path('products/limited/', limitid, name='limitid'),
    path('sales/', slayer, name='slayer'),
    path('basket/', basket, name='basket'),
    
]