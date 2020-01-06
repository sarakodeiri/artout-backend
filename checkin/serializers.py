from rest_framework import serializers
from . import models
from user import serializers as user_serializers
from event import serializers as event_serializers


class CheckinSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()

    class Meta:
        model = models.CheckIn
        fields = ['event', 'user', 'submitted_time', 'go_time']
        read_only_fields = ('event', 'user')

    def get_user(self, obj):
        user_serializer = user_serializers.UserPreviewSerializer(obj.user)
        return user_serializer.data

    def get_event(self, obj):
        event_serializer = event_serializers.EventSerializer(obj.event)
        return event_serializer.data
