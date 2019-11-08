from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django.core.exceptions import *
from django.http import JsonResponse, HttpResponseBadRequest


class EventListID(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('id', '')
        if user_id is '':
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            try:
                user = UserProfile.objects.get(id=user_id)
                user_events = Event.objects.filter(event_owner=user)
                event_ids = [event.id for event in user_events]
                return Response(event_ids, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response("User not found!", status=status.HTTP_404_NOT_FOUND)


class EventListDetail(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('id', '')
        if user_id is '':
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            try:
                user = UserProfile.objects.get(id=user_id)
                user_events = Event.objects.filter(event_owner=user)

                page = self.paginate_queryset(user_events)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(user_events, many=True)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response("User not found!", status=status.HTTP_404_NOT_FOUND)


class EventDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()

class EventCheckin(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CheckinSerializer

    def post(self, request, *args, **kwargs):
        user = UserProfile.objects.get(id= request.data['user'])
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