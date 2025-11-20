from rest_framework import viewsets
from .models import UserInfo
from .serializers import SignInSerializer, SignUpSerializer, SignOutSerializer

class SignInAPIView(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = SignInSerializer
    http_method_names = ['post']

class SignUpAPIView(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = SignUpSerializer
    http_method_names = ['post']

class SignOutAPIView(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = SignOutSerializer
    http_method_names = ['post']