from django.shortcuts import render
from rest_framework import generics


class EventList(generics.ListCreateAPIView):
    pass


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    pass
