from django.utils.six import text_type
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from user import models


class RegisterSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfile
        fields = ('email', 'first_name', 'last_name', 'date_joined', 'avatar', 'username','password', 'tokens')
        extra_kwargs = {'password': {'write_only': True}}

    def get_tokens(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = text_type(tokens)
        access = text_type(tokens.access_token)
        data = {
            "refresh": refresh,
            "access": access
        }
        return data

    def create(self, validated_data):
        return models.UserProfile.objects.create_user(username=validated_data.get("username"),
                                                      email=validated_data.get("email"),
                                                      password=validated_data.get("password"),
                                                      first_name=validated_data.get("first_name"),
                                                      last_name=validated_data.get("last_name"),
                                                      avatar=validated_data.get("avatar"))


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = user.id

        return token
