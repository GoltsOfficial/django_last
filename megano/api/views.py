from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
import json

from api.serializers import UserRegistrationSerializer


@api_view(['POST'])
@csrf_exempt
def sign_up(request):
    data = json.loads(request.body)
    serializer = UserRegistrationSerializer(data=data)

    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)