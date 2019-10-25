from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from Artout.user import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('email', 'first_name', 'last_name', 'date_joined', 'avatar', 'username','id')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('email', 'first_name', 'last_name', 'date_joined', 'avatar', 'username','password')

    def create(self, validated_data):
        return models.UserProfile.objects.create_user(username=validated_data["username"], email=validated_data["email"], password=validated_data["password"],first_name=validated_data["first_name"],last_name=validated_data["last_name"],avatar=validated_data["avatar"])


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = user.id

        return token
