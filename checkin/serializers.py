from rest_framework import serializers
from . import models
from user import serializers as user_serializers
from event import serializers as event_serializers


class CheckinSerializer(serializers.ModelSerializer):
    checkin_user = serializers.SerializerMethodField()
    checkin_event = serializers.SerializerMethodField()

    class Meta:
        model = models.CheckIn
        fields = ['event', 'user', 'submitted_time', 'go_time', 'checkin_event', 'checkin_user']

    def get_checkin_user(self, obj):
        kwargs = {}
        kwargs['context'] = self.context
        user_serializer = user_serializers.UserPreviewSerializer(obj.user, **kwargs)
        return user_serializer.data

    def get_checkin_event(self, obj):
        kwargs = {}
        kwargs['context'] = self.context
        event_serializer = event_serializers.EventPreviewSerializer(obj.event, **kwargs)
        return event_serializer.data
