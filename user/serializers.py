from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'avatar', 'username', 'is_private')
        read_only_fields = ('is_private',)


class UserPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.UserProfile
        fields = ('id', 'fist_name', 'last_name', 'username')