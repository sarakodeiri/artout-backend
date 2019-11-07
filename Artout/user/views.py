
from rest_framework import generics
from Artout.user import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from Artout.user.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


class RegisterView(generics.CreateAPIView):
    """
        Register a new user with the user data
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            serializer_user = serializers.UserSerializer(user)
            data = {"id": serializer_user.data["id"]}
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    """
        Get Refresh And Access Token by Username and Password Given
    """
    serializer_class = serializers.LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = UserProfile.objects.get(username=request.data['username'])
        if serializer.is_valid():
            serializer.validated_data['id'] = user.id
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    permission_class = (AllowAny,)
    serializer_class = serializers.UserSerializer
    queryset = UserProfile.objects.all()