from .views import EventList, EventDetail
from django.urls import path

urlpatterns = [
    path('<int:eid>/', EventDetail.as_view()),
    path('', EventList.as_view()),
]