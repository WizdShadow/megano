from django.contrib import admin
from .models import Category, Product, ProductImages, Tags, ProductTask, Reviews, Specifications, SpecificationsProduct, Timeuser

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]

@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImages._meta.fields]

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tags._meta.fields]

@admin.register(ProductTask)
class ProductTaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductTask._meta.fields]

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Reviews._meta.fields]

@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Specifications._meta.fields]

@admin.register(SpecificationsProduct)
class SpecificationsProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SpecificationsProduct._meta.fields]

@admin.register(Timeuser)
class TimeuserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Timeuser._meta.fields]