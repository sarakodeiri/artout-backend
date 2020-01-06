from django.urls import path
from . import views


urlpatterns = [

    path('checkin/', views.CheckinList.as_view()),
    path('checkin/<int:id>', views.CheckinDetail.as_view()),

]
