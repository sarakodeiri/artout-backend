from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models as follow_models
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

    def get_queryset(self):
        return follow_models.Follow.objects.select_related('followee').filter(follower=self.request.user)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, followee__id=self.kwargs['uid'])
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        follower =self.request.user
        removed = follow_models.Follow.objects.remove_following(follower, instance)
        if removed:
            return Response("User successfully unfollowed", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You don't follow this user", status=status.HTTP_404_NOT_FOUND)


class FollowersDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = user_serializers.UserSerializer

    def get_queryset(self):
        return follow_models.Follow.objects.select_related('follower').filter(followee=self.request.user)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, follower__id=self.kwargs['uid'])
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        followee =self.request.user
        removed = follow_models.Follow.objects.remove_following(instance, followee)
        if removed:
            return Response("User successfully removed from your follower's list", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("This user doesn't follow you", status=status.HTTP_404_NOT_FOUND)