from django.urls import path
from . import views


urlpatterns = [
    path('followings/', views.FollowingsList.as_view()),
]
