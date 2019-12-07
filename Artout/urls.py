from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1.0/events/', include('event.urls')),
    path('api/v1.0/users/', include('user.urls')),
    path('api/v1.0/authentication/', include('authentication.urls')),
]
