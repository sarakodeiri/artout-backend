from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer, CheckinSerializer
from .models import Event, UserProfile, CheckIn
from django.core.exceptions import *
from django.http import JsonResponse, HttpResponseBadRequest


class EventList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_queryset(self):
        user = get_object_or_404(UserProfile, pk=self.kwargs['owner'])
        return Event.objects.filter(owner__id=user.id)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        data["owner"] = user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EventDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer


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
