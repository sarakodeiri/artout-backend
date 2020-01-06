from rest_framework import serializers
from . import models


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ('id', 'longitude', 'latitude')


class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = models.Event
        fields = ('id', 'title', 'description', 'start_date', 'end_date', 'picture_url', 'owner', 'location', 'category')

    def create(self, validated_data):
        location = validated_data.pop('location')
        location = models.Location.objects.create(**location)
        validated_data['location'] = location
        event = models.Event.objects.create(**validated_data)
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
        models.Location.objects.update(**location)
        instance.save()
        return instance



