from django.contrib import admin
from .models import Event
# from .models import Location
from .models import CheckIn


admin.site.register(Event)
# admin.site.register(Location)
admin.site.register(CheckIn)
