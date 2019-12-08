from .views import EventList, EventCheckinList, EventDetail, EventCheckinDetail
from django.urls import path

urlpatterns = [
    path('<int:eid>/', EventDetail.as_view()),
    path('', EventList.as_view()),
    path('<int:eid>/checkins/', EventCheckinList.as_view()),
    path('<int:eid>/checkins/<int:cid>', EventCheckinDetail.as_view())
]