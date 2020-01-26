from rest_framework.permissions import BasePermission
from rest_framework.generics import get_object_or_404

from follow import models as follow_models
from user import models as user_models
from event import models as event_models


class EventPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        followings = follow_models.Follow.objects.filter(
            follower=request.user).values_list("followee_id", flat=True)
        public_users = user_models.UserProfile.objects.filter(is_private=False).values_list("id", flat=True)
        ids = list(followings) + list(public_users) + [request.user.id]
        event_id = request.data.get("event_id")
        event = get_object_or_404(event_models.Event, pk=event_id)
        return event.owner_id in ids
