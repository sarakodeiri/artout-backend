from .views import EventList, EventCheckin, EventDetail, EventCheckinDetail
from django.urls import path

urlpatterns = [
    path('<int:id>/', EventDetail.as_view()),
    path('', EventList.as_view()),
    path('<int:id>/checkins/', EventCheckin.as_view()),
    path('<int:id>/checkins/<int:cd>', EventCheckinDetail.as_view())
]