from rest_framework import generics
from user import serializers
from rest_framework.permissions import AllowAny
from user.models import UserProfile


class UserList(generics.ListAPIView):
    permission_class = (AllowAny,)
    serializer_class = serializers.UserSerializer
    queryset = UserProfile.objects.all()