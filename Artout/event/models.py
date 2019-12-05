from django.db import models
from Artout.user.models import UserProfile


class Location(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    picture_url = models.CharField(null=True, blank=True, max_length=2000)
    event_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class CheckIn(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    check_in_time = models.DateField()
    go_time = models.DateField()



