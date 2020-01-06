from rest_framework import serializers
from . import models


class CheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CheckIn
        fields = '__all__'