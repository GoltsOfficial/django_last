from django.contrib import admin
from .models import Category, Product, ProductImage, Tag, Review, Sale

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']
    list_filter = ['parent']
    search_fields = ['title']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'count', 'rating', 'available']
    list_filter = ['category', 'available', 'limited_edition']
    search_fields = ['title', 'description']
    inlines = [ProductImageInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'date']
    list_filter = ['rating', 'date']
    search_fields = ['product__title', 'user__username']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'salePrice', 'dateFrom', 'dateTo']
    list_filter = ['dateFrom', 'dateTo']
    search_fields = ['product__title']