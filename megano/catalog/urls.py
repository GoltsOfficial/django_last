from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories),
    path('catalog/', views.catalog),
    path('products/popular/', views.popular_products),
    path('products/limited/', views.limited_products),
    path('sales/', views.sales),
    path('banners/', views.banners),
    path('product/<int:id>/', views.product_detail),
    path('product/<int:id>/review/', views.product_review),
]
