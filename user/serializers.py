from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('email', 'first_name', 'last_name', 'date_joined', 'avatar', 'username')