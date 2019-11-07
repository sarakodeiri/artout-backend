from django.contrib import admin
from django.urls import path, include
from Artout.user.views import RegisterView
from rest_framework_simplejwt import views as jwt_views
from Artout.user.views import LoginView


urlpatterns = [
    path('', include('Artout.user.urls')),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('event/', include('Artout.event.urls')),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]