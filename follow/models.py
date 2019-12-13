from django.db import models

from user.models import UserProfile


class FollowRequestManager(object):
    pass


class FollowRequest(models.Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="follow_pendings")
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="follow_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    objects = FollowRequestManager()

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
        follow_objects = Follow.objects.select_related('follower').filter(followee=user)
        followers = [follow_object.follower for follow_object in follow_objects]
        return followers

    def followings(self, user):
        follow_objects = Follow.objects.select_related('followee').filter(follower=user)
        followees = [follow_object.followee for follow_object in follow_objects]
        return followees

    def add_follower(self, from_user, to_user):
        if to_user.is_private:
            return FollowRequest.objects.create(follower=from_user, followee=to_user), "Requested"
        else:
            return Follow.objects.create(from_user=from_user, to_user=to_user), "Added"

    def remove_follower(self, follower, followee):
        try:
            Follow.objects.get(followee=followee, follower=follower).delete()
            return True
        except models.ObjectDoesNotExist:
            return False

    def requests(self, user):
        follow_request_objects = FollowRequest.objects.select_related('from_user').filter(to_user=user)
        requests = [follow_request_object.from_user for follow_request_object in follow_request_objects]
        return requests

    def pendings(self, user):
        follow_request_objects = FollowRequest.objects.select_related('to_user').filter(from_user=user)
        pendings = [follow_request_object.to_user for follow_request_object in follow_request_objects]
        return pendings

    def is_follower(self, follower, followee):
        return Follow.objects.filter(follower=follower, followee=followee).exists()


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="followings")
    followee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    objects = FollowManager()


