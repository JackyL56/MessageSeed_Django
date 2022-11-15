from django.shortcuts import render

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics


# Used to modify and add information to JWT payload
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# View for registering new user
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

