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
        fields = ('title', 'description', 'start_date', 'end_date', 'picture_url', 'event_owner', 'location', 'category')

    def create(self, validated_data):
        location = validated_data.pop('location')
        event = models.Event.objects.create(**validated_data)
        location = models.Location.objects.create(**location)
        event.location = location
        event.save()
        return event

    def update(self, instance, validated_data):
        location = validated_data.pop('location')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.picture_url = validated_data.get('picture_url', instance.picture_url)
        instance.category = validated_data.get('category', instance.category)
        if location is not None:
            instance.location = Location(longitude=location['longitude'],latitude=location['latitude'])
        return instance


class CheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CheckIn
        fields = '__all__'
