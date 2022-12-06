from django.contrib import admin
from .serializers import UserSerializer, GroupSerializer

# Register your models here.
admin.register(UserSerializer)
admin.register(GroupSerializer)
