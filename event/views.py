from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from . import models


class EventList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        owner_id = self.request.query_params.get('owner')
        if owner_id is None:
            owner_id = self.request.user.id
        return models.Event.objects.filter(owner_id=owner_id)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        data["owner"] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()

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


class EventCheckinList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CheckinSerializer

    def get_queryset(self):
        event_id = self.kwargs.get('eid')
        event = get_object_or_404(models.Event, id=event_id)
        return models.CheckIn.objects.filter(event=event)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        data["user"] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EventCheckinDetail(generics.DestroyAPIView):
    queryset = models.CheckIn.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['cid'])
        if self.request.user != obj.owner:
            return HttpResponseForbidden()
        self.check_object_permissions(self.request, obj)
        return obj
