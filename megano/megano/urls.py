from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('api/', include('api.urls')),  # Добавляем api маршруты
    path('api/', include('catalog.urls')),  # эндпоинты каталога
]
