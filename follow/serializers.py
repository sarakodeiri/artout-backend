from rest_framework import serializers
from . import models


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FollowRequest
        fields = ('from_user', 'to_user')
