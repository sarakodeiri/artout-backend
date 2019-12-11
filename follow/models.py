from django.db import models

from user.models import UserProfile


class FollowRequest(models.Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="follow_pending")
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="follow_request")
    created = models.DateTimeField(auto_now_add=True)

    def accept(self):
        Follow.objects.create(follower=self.from_user, followee=self.to_user)
        self.delete()
        return True

    def reject(self):
        self.delete()
        return True

    def cancel(self):
        self.delete()
        return True


class FollowManager(models.Manager):

    def followers(self, user):
        return Follow.objects.filter(followee=user)

    def followings(self, user):
        return Follow.objects.filter(follower=user)

    def follower(self, from_user, to_user):
        if to_user.is_private:
            return FollowRequest.objects.create(follower=from_user, followee=to_user), "Requested"
        else:
            return Follow.objects.create(from_user=from_user, to_user=to_user), "Added"

    def unfollow(self, follower, followee):
        if self.is_follower(follower,followee):
            Follow.objects.get(followee=followee, follower=follower).delete()
            return True
        else:
            return False

    def requests(self, user):
        return FollowRequest.objects.filter(to_user=user)

    def pendings(self, user):
        return FollowRequest.objects.filter(from_user=user)

    def is_follower(self, follower, followee):
        return Follow.objects.filter(follower=follower, followee=followee).exists()


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="followings")
    followee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True)
    object = FollowManager()


