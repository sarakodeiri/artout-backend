from functools import cmp_to_key

from django.db import models

from follow import models as follow_models
from user import models as user_models
from checkin import models as checkin_models
from event import models as event_models


def compare(item1, item2):
    if len(item1.last_checkin) > 0 :
        time1 = item1.last_checkin[-1].submitted_time
    else:
        time1 = item1.created_at
    if len(item2.last_checkin) > 0:
        time2 = item2.last_checkin[-1].submitted_time
    else:
        time2 = item1.created_at

    if time1 > time2:
        return -1
    elif time1 == time2:
        return 0
    return 1


class EventManager(models.Manager):
    def get_timeline_events(self, user):
        followings = follow_models.Follow.objects.filter(
            follower=user).values_list("followee_id", flat=True)
        public_users = user_models.UserProfile.objects.filter(is_private=False).values_list("id", flat=True)
        ids = list(followings) + list(public_users) + [user.id]

        queryset = checkin_models.CheckIn.objects.filter(user_id__in=followings).order_by('submitted_time')

        followees_events = event_models.Event.objects.filter(models.Q(owner_id__in=followings) |
                                                (models.Q(checkins__user_id__in=ids) &
                                                 models.Q(owner_id__in=ids)))\
            .annotate(checkin_count=models.Count('checkins')).prefetch_related(
                                                 models.Prefetch('checkins', queryset, to_attr='last_checkin'))

        ordered = sorted(followees_events, key=cmp_to_key(compare))

        return ordered
