from django.db import models

from follow import models as follow_models
from user import models as user_models
from checkin import models as checkin_models
from event import models as event_models


class EventManager(models.Manager):
    def compare(self, item1, item2):
        if item1.checkin is not None:
            time1 = item1.checkin.submitted_time
        else:
            time1 = item1.created_at
        if item2.checkin is not None:
            time2 = item1.checkin.submitted_time
        else:
            time2 = item1.created_at

        if time1 > time2:
            return 1
        elif time1 == time2:
            return 0
        return -1

    def get_timeline_events(self, user):
        followings = follow_models.Follow.objects.filter(
            follower=user).values_list("followee_id", flat=True)
        public_users = user_models.UserProfile.objects.filter(is_private=False).values_list("id", flat=True)
        ids = list(followings) + list(public_users) + [user.id]

        queryset = checkin_models.CheckIn.objects.filter(user_id__in=followings).order_by('submitted_time').last()

        followees_events = event_models.Event.objects.filter(models.Q(owner_id__in=followings) |
                                                (models.Q(checkins__user_id__in=ids) &
                                                 models.Q(owner_id__in=ids))).prefetch_related(
                                                 models.Prefetch('checkins', queryset))
        ordered = sorted(followees_events, key=lambda x,y: EventManager.compare(x,y))

        return ordered
