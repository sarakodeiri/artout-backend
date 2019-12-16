from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from user.models import UserProfile
from user import serializers


class UserList(generics.ListAPIView):
    permission_class = (IsAdminUser,)
    serializer_class = serializers.UserSerializer
    queryset = UserProfile.objects.all()


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    queryset = UserProfile.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, username=self.kwargs['uname'])
        self.check_object_permissions(self.request, obj)
        return obj

