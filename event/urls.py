from .views import EventList, EventDetail, Timeline
from django.urls import path

urlpatterns = [
    path('<int:eid>/', EventDetail.as_view()),
    path('', EventList.as_view()),
    path('timeline/', Timeline.as_view())
]