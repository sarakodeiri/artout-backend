from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from user.models import UserProfile
from user import serializers


class UserList(generics.ListAPIView):
    permission_class = (IsAdminUser,)
    serializer_class = serializers.UserSerializer
    queryset = UserProfile.objects.all()

