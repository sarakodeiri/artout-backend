from django.db import models

from user.models import UserProfile


class FollowRequest(models.Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="follow_pending")
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="follow_request")
    created = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="following")
    followee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True)

