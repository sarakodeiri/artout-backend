from rest_framework import serializers
from . import models
from follow import models as follow_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'avatar', 'username', 'is_private')


class UserPreviewSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    class Meta:
        model = models.UserProfile
        fields = ('id', 'first_name', 'last_name', 'username', 'avatar', 'state')

    def get_state(self, obj):
        user = self.context['request'].user
        if user == obj:
            return 0
        elif follow_models.Follow.objects.filter(followee=obj, follower=user).exists():
            return 1
        elif follow_models.FollowRequest.objects.filter(to_user=obj, from_user=user).exists():
            return 2
        else:
            return 3


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    events_count = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfile
        fields = ('id', 'first_name', 'last_name', 'username', 'date_joined', 'avatar', 'is_private',
                  'followers_count', 'followings_count', 'events_count', 'state')

    def get_followers_count(self, obj):
        return obj.followers_count

    def get_followings_count(self, obj):
        return obj.followings_count

    def get_events_count(self, obj):
        return obj.events_count

    def get_state(self, obj):
        user = self.context['request'].user
        if user == obj:
            return 0
        elif follow_models.Follow.objects.filter(followee=obj, follower=user).exists():
            return 1
        elif follow_models.FollowRequest.objects.filter(to_user=obj, from_user=user).exists():
            return 2
        else:
            return 3
