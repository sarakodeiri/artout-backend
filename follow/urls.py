from django.urls import path
from . import views


urlpatterns = [

    path('followings/', views.FollowingsList.as_view()),
    path('followers/', views.FollowersList.as_view()),
    path('followings/<int:uid>/', views.FollowingsDetail.as_view()),
    path('followers/<int:uid>/', views.FollowersDetail.as_view()),
    path('followings/pendings/', views.PendingsList.as_view()),
    path('followers/requests/', views.RequestsList.as_view()),
    path('followings/pendings/<int:uid>/', views.PendingsDetail.as_view()),
    path('followers/requests/<int:uid>/', views.RequestsDetail.as_view()),
]
