from .views import EventList
from django.urls import path

urlpatterns = [
    path('events/', EventList.as_view()),
]