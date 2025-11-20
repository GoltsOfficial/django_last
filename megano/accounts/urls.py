from django.urls import path
from .views import (
    SignInAPIView,
    SignUpAPIView,
    SignOutAPIView
)


urlpatterns = [
    path("/sign-in/", SignInAPIView.as_view(), name="sign-in"),
    path("/sign-up/", SignUpAPIView.as_view(), name="sign-up"),
    path("/sign-out/", SignOutAPIView.as_view(), name="sign-out"),
]
