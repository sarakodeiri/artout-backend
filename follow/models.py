from django.db import models

from user.models import UserProfile


class FollowRequest(models.Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="follow_pending")
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="follow_request")
    created = models.DateTimeField(auto_now_add=True)

    def accept(self):
        follow = Follow.objects.create(follower=self.from_user, followee=self.to_user)
        self.delete()
        return True

    def reject(self):
        self.delete()
        return True

    def cancel(self):
        self.delete()
        return True


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="following")
    followee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True)

