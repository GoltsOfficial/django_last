from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout as auth_logout

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


@api_view(['POST'])
@csrf_exempt
def sign_in(request):
    data = json.loads(request.body)

    user = authenticate(
        request,
        username=data.get('username'),
        password=data.get('password')
    )

    if user is not None:
        login(request, user)
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    else:
        return Response(
            {'status': 'error', 'message': 'Invalid credentials'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@csrf_exempt
def sign_out(request):
    auth_logout(request)
    return Response({'status': 'success'})