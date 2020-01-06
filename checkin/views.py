from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from url_filter.integrations.drf import DjangoFilterBackend

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from . import models


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