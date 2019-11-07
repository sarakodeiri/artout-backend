from django.db import models
from Artout.user.models import UserProfile


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField()
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    rate = models.IntegerField(blank=True, max_length=5)
    picture = models.CharField(blank=True, max_length=2000)
    event_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)



class CheckIn(models.Model):
    pass


class Location(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
