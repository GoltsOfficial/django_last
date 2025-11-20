from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('catalog.urls')),
    path('', include('basket.urls')),
    path('', include('orders.urls')),
    path('', include('payment.urls')),
    path('', include('frontend.urls')),
]