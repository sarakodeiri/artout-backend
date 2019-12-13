from django.urls import path
from . import views


urlpatterns = [
    path('followings/pendings/', views.PendingsList.as_view()),
    path('followers/requests/', views.RequestsList.as_view()),
    path('followings/pendings/<int:uid>/', views.PendingsDetail.as_view()),
    path('followers/requests/<int:uid>/', views.RequestsDetail.as_view()),

]
