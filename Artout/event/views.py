from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django.http import JsonResponse, HttpResponseBadRequest


class EventList(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('id', None)
        if user_id is None:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        user = UserProfile.objects.get(id = user_id)
        user_events = Event.objects.filter(event_owner=user)
        event_ids = [event.id for event in user_events]
        return Response(event_ids, status=status.HTTP_200_OK)

    def get(self, request):
        # is_authenticated = request.user.is_authenticated()
        #
        # if not is_authenticated:
        #     return HttpResponseBadRequest()

        user_id = 3
        all_events = Event.objects.filter(event_owner_id=user_id)
        serializer = EventSerializer(all_events, many=True)
        return JsonResponse({"all_events": serializer.data})


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    pass
