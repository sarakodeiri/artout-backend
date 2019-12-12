from django.urls import path
from . import views


urlpatterns = [
    path('followings/', views.FollowingsList.as_view()),
    path('followers/', views.FollowersList.as_view()),
    path('followings/<int:uid>/', views.FollowingsDetail.as_view()),
]
