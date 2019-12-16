from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserList.as_view()),
    path('username/<str:username>', views.UserDetail.as_view())
]
