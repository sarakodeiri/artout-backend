from django.db import models

from event.models import Event
from user.models import UserProfile


class CheckIn(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    submitted_time = models.DateTimeField(auto_now_add=True)
    go_time = models.DateTimeField()
