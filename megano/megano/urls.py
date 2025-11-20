from django.urls import path, include
from django.contrib import admin
from rest_framework import routers

from accounts.views import SignUpAPIView, SignInAPIView, SignOutAPIView


router = routers.DefaultRouter()
router.register(r'sign-in', SignInAPIView, basename='sign-in')
router.register(r'sign-up', SignUpAPIView, basename='sign-up')
router.register(r'sign-out', SignOutAPIView, basename='sign-out')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('api/', include(router.urls)),
]
