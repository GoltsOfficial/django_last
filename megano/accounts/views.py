from rest_framework import viewsets

from .models import UserInfo
from .serializers import UserInfoSerializer
'''
# URLs
/sign-in/              # POST
/sign-up/              # POST
/sign-out/             # POST
/profile/              # GET, POST
/profile/password/     # POST
/profile/avatar/       # POST
'''

class UserInfoAPIView(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    http_method_names = ['post']
