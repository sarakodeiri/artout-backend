from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    avatar = models.CharField(blank=True, max_length=2000)
    device_token = models.CharField(blank=True, max_length=2000)
    is_private = models.BooleanField(default=True)
