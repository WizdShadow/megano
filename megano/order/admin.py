from django.contrib import admin
from .models import OrderModel, OrderProdcut

# Register your models here.
@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderModel._meta.fields]

@admin.register(OrderProdcut)
class OrderProdcutAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderProdcut._meta.fields]