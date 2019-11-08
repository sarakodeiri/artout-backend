from .views import *
from django.urls import path

urlpatterns = [
    path('events/', EventListID.as_view()),
    path('eventsd/', EventListDetail.as_view()),
    path('eventdetail/<int:pk>/', EventDetail.as_view())
]