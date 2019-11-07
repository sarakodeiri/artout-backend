from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django.http import JsonResponse, HttpResponseBadRequest


class EventList(generics.ListCreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = EventSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            event = serializer.save()
            serializer_event = EventSerializer(event)
            data = {"event": serializer_event.data}
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
