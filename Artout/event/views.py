from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer, CheckinSerializer
from .models import Event, UserProfile, CheckIn
from django.http import HttpResponseForbidden

from django.core.exceptions import *
from django.http import JsonResponse, HttpResponseBadRequest


class EventList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_queryset(self):
        owner_id = self.request.query_params.get('owner')
        return Event.objects.filter(owner_id=owner_id)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        data["owner"] = user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(id=self.kwargs['eid'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.user == instance.owner:
            return HttpResponseForbidden()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class EventCheckinList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CheckinSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        data["user"] = user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EventCheckinDetail(generics.DestroyAPIView):
    pass
