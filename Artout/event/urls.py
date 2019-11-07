from .views import *
from django.urls import path

urlpatterns = [
    path('events/', EventList.as_view()),
    path('eventdetail/<int:pk>/', EventDetail.as_view())
]