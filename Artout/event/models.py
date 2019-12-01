# from django.contrib.gis.db import models
from django.db import models
from Artout.user.models import UserProfile


class Location(models.Model):
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    rate = models.IntegerField(blank=True, null=True)
    picture_url = models.CharField(null=True, blank=True, max_length=2000)
    event_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(blank=True, null=True, max_length=20)


    def __str__(self):
        return self.title


class CheckIn(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    check_in_time = models.DateTimeField()
    go_time = models.DateTimeField()

    def __str__(self):
        return "CheckIn to " + self.event.title



