from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from url_filter.integrations.drf import DjangoFilterBackend
from django.db import models as db_models


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from . import models
from follow import models as follow_models
from user import models as user_models


class EventList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['title', 'owner', 'start_date', 'end_date', 'description', 'category']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.EventCreationSerializer
        else:
            return serializers.EventSerializer

    def get_queryset(self):
        followings = follow_models.Follow.objects.filter(follower=self.request.user).values_list(
            "followee_id", flat=True)
        public_users = user_models.UserProfile.objects.filter(is_private=False).values_list("id", flat=True)
        ids = list(followings) + list(public_users) + [self.request.user.id]
        return models.Event.objects.filter(owner__in=ids).annotate(checkin_count=db_models.Count('checkins'))

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        data["owner"] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data["url"] = serializer.instance.url
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all().annotate(checkin_count=db_models.Count('checkins'))

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['eid'])
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.user != instance.owner:
            return HttpResponseForbidden()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.owner:
            return HttpResponseForbidden()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class Timeline(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.EventSerializer

    def get_queryset(self):
        qs = models.Event.objects.get_timeline_events(self.request.user)
        return qs

    def paginate_queryset(self, queryset):
        page_size = self.request.GET.get('page_size')
        paginator = Paginator(queryset, page_size)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj

    def get_paginated_response(self, data):
        return Response(data)
