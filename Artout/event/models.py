from django.db import models
from Artout.user.models import UserProfile


class Location(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    rate = models.IntegerField(blank=True)
    picture = models.CharField(blank=True, max_length=2000)
    event_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)


class CheckIn(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    check_in_time = models.DateField()
    go_time = models.DateField()



