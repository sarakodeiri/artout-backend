from django.contrib.gis.db import models
from Artout.user.models import UserProfile


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    rate = models.IntegerField(blank=True, null=True)
    picture_url = models.CharField(null=True, blank=True, max_length=2000)
    event_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    location = models.PointField()
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class CheckIn(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    check_in_time = models.DateField()
    go_time = models.DateField()



