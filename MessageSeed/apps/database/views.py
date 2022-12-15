# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.database.serializers import UserSerializer, GroupSerializer
from apps.database.models import Author, Message


class UserViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows users to be viewed or edited. """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class AuthorViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows authors to be viewed or edited. """
    queryset = Author.objects.all()
    # permission_classes = [IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows messages to be viewed or edited. """
    queryset = Message.objects.all()
    # permission_classes = [IsAuthenticated]

