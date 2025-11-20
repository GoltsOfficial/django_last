from rest_framework import serializers
from .models import UserInfo

class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('name', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class SignOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ()  # пустые поля или можно указать 'id'