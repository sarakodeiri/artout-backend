from .views import EventList, EventCheckinList, EventDetail, EventCheckinDetail
from django.urls import path

urlpatterns = [
    path('<int:id>/', EventDetail.as_view()),
    path('', EventList.as_view()),
    path('<int:id>/checkins/', EventCheckinList.as_view()),
    path('<int:id>/checkins/<int:cd>', EventCheckinDetail.as_view())
]