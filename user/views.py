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


class UserDetail(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    queryset = UserProfile.objects.all()

    def get_object(self):
        try:
            user = UserProfile.objects.get(username=self.kwargs['un'])
            id = user.id
            return Response(id, status=status.HTTP_200_OK)
        except user.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

