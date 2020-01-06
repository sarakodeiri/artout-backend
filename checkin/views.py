from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from url_filter.integrations.drf import DjangoFilterBackend

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from . import models
from follow import models as follow_models
from user import models as user_models


class CheckinList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CheckinSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user', 'event', 'go_time', 'submitted_time']

    def get_queryset(self):
        followings = follow_models.Follow.objects.filter(
            follower=self.request.user).values_list("followee_id", flat=True)
        public_users = user_models.UserProfile.objects.filter(is_private=False).values_list("id", flat=True)
        ids = list(followings) + list(public_users) + [self.request.user.id]
        return models.CheckIn.objects.filter(user_id__in=ids, event__owner__in=ids).select_related("user", "event")

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        data["user"] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CheckinDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CheckIn.objects.all().select_related("user", "event")
    serializer_class = serializers.CheckinSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['id'])
        if self.request.user != obj.owner:
            return HttpResponseForbidden()
        self.check_object_permissions(self.request, obj)
        return obj