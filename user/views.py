from django.db import models as db_models
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated


from user.models import UserProfile
from user import serializers
from follow import models as follow_models


class UserList(generics.ListAPIView):
    permission_class = (IsAdminUser,)
    serializer_class = serializers.UserSerializer
    queryset = UserProfile.objects.all()


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    queryset = UserProfile.objects.all()
    lookup_field = "username"


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserProfileSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user', self.request.user.id)

        user = UserProfile.objects.filter(id=user_id).annotate(followers_count=db_models.Count('followers'),
                                                               followings_count=db_models.Count('followings'),
                                                               events_count=db_models.Count('events'))
        return user

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        user_id = self.request.query_params.get('user', self.request.user.id)
        obj = get_object_or_404(queryset, pk=user_id)
        return obj
