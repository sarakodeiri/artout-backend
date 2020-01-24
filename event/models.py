from django.db import models
from user.models import UserProfile

from . import managers


class Location(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    picture_exists = models.BooleanField(default=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='events')
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    category = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = managers.EventManager()

    def __str__(self):
        return self.title
