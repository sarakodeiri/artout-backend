from rest_framework import serializers
from Artout.event import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ('title', 'description', 'start_date', 'end_date', 'picture_url', 'event_owner', 'location')


class CheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CheckIn
        fields = '__all__'
