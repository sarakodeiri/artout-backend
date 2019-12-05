from .views import *
from django.urls import path

urlpatterns = [
    path('events/<int:id>/', EventList.as_view()),
    path('checkin/', EventCheckin.as_view()),
]