from django.db import models

from event.models import Event
from user.models import UserProfile


class CheckIn(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="checkins")
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="checkins")
    submitted_time = models.DateTimeField(auto_now_add=True)
    go_time = models.DateTimeField()
