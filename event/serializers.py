from rest_framework import serializers
from . import models
from checkin import models as checkin_models
from .managers import EventPictureManager


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ('id', 'longitude', 'latitude')


class EventCreationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    picture_manager = EventPictureManager()
    s3_response = serializers.SerializerMethodField()

    def get_s3_response(self, obj):
        if obj.picture_exists:
            picture_url = self.picture_manager.create_post_url(obj.id)
            return picture_url

    class Meta:
        model = models.Event
        fields = ('id', 'title', 'description', 'start_date', 'end_date', 'picture_exists', 'owner', 'location',
                  'category', 's3_response')

    def create(self, validated_data):
        location = validated_data.pop('location')
        location = models.Location.objects.create(**location)
        validated_data['location'] = location
        event = models.Event.objects.create(**validated_data)
        event.save()
        return event


class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    checkin_count = serializers.SerializerMethodField()
    is_checked_in = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        fields = ('id', 'title', 'description', 'start_date', 'end_date', 'picture_url', 'owner', 'location',
                  'category', 'checkin_count', 'is_checked_in')

    def get_checkin_count(self, obj):
        return obj.checkin_count

    def get_is_checked_in(self, obj):
        return checkin_models.CheckIn.objects.filter(user=self.context["request"].user, event=obj).exists()

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


class EventPreviewSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    is_checked_in = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        fields = ('id', 'title', 'description', 'start_date', 'end_date', 'picture_url', 'owner', 'location',
                  'category', 'is_checked_in')

    def get_is_checked_in(self, obj):
        return checkin_models.CheckIn.objects.filter(user=self.context["request"].user, event=obj).exists()
