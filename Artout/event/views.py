from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django.core.exceptions import *
from django.http import JsonResponse, HttpResponseBadRequest


class EventList(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        user = get_object_or_404(UserProfile, pk=self.kwargs['id'])
        return Event.objects.filter(owner__id=user.id)


class EventDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventCheckin(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CheckinSerializer

    def post(self, request, *args, **kwargs):
        user = UserProfile.objects.get(id=request.data['user'])
        event = Event.objects.get(id=request.data['event'])
        if CheckIn.objects.filter(event=event, user=user).exists():
            CheckIn.objects.get(event=event, user=user).delete()
            return Response('Unchecked', status=status.HTTP_200_OK)
        else:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response('Checked-in', status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
