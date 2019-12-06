from .views import EventList, EventCheckin, EventDetail
from django.urls import path

urlpatterns = [
    path('<int:id>/', EventDetail.as_view()),
    path('/', EventList.as_view()),
    path('<int:id>/checkin/', EventCheckin.as_view()),
]