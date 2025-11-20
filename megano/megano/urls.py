from django.urls import path, include
from django.contrib import admin
from rest_framework import routers

from accounts.views import UserInfoAPIView

router = routers.DefaultRouter()
router.register('api/sign-up', UserInfoAPIView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('', include(router.urls)),
]
