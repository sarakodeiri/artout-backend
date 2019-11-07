from rest_framework import serializers
from Artout.event import models
from Artout.event.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ('longitude', 'latitude')


class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = models.Event
        fields = ('title', 'description', 'start_date', 'end_date', 'picture_url', 'event_owner', 'location')

    def create(self, validated_data):
        location = validated_data.pop('location')
        event = models.Event.objects.create(**validated_data)
        location = models.Location.objects.create(**location)
        event.location = location
        event.save()
        return event


class CheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CheckIn
        fields = '__all__'
