from django.contrib import admin
from .models import Category, Tag, Banner


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Регистрация модели Категории товара"""

    list_display = ["title", "src", "alt", "parent"]
    list_filter = ["title", "parent"]
    search_fields = ["title"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Регистрация модели тэга товара"""

    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'active']
    list_editable = ['order', 'active']