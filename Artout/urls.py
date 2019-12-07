from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1.0/events', include('Artout.event.urls')),
    path('api/v1.0/users', include('Artout.user.urls'))
]
