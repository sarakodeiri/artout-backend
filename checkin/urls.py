from django.urls import path
from . import views


urlpatterns = [
    path('', views.CheckinList.as_view()),
    path('<int:id>/', views.CheckinDetail.as_view()),
]
