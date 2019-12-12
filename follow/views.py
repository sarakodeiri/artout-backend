from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from follow import models as follow_models
from user import serializers as user_serializers
from user import models as user_models


class FollowingsList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = user_serializers.UserPreviewSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user')
        if user_id is None:
            user = self.request.user
            return follow_models.Follow.objects.followings(user)
        else:
            user = get_object_or_404(user_models.UserProfile, id=user_id)
            if not user.is_private or follow_models.Follow.objects.is_follower(self.request.user, user):
                return follow_models.Follow.objects.followings(user)
            else:
                return self.permission_denied(self.request, message="This user is private")


class FollowersList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = user_serializers.UserPreviewSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user')
        if user_id is None:
            user = self.request.user
            return follow_models.Follow.objects.followers(user)
        else:
            user = get_object_or_404(user_models.UserProfile, id=user_id)
            if not user.is_private or follow_models.Follow.objects.is_follower(self.request.user, user):
                return follow_models.Follow.objects.followers(user)
            else:
                return self.permission_denied(self.request, message="This user is private")


class FollowingsDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = user_serializers.UserSerializer
    queryset = user_models.UserProfile.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['uid'])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_destroy(self, instance):
        follower = self.request.user
        follow_models.Follow.objects.remove_follower(follower, instance)


class FollowersDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = user_serializers.UserSerializer
    queryset = user_models.UserProfile.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['uid'])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_destroy(self, instance):
        followee = self.request.user
        follow_models.Follow.objects.remove_follower(instance, followee)
