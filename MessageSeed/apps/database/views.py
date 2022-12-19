# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from apps.database.serializers import *
from apps.database.models import *


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
    serializer_class = AuthorSerializer
    # permission_classes = [IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows messages to be viewed or edited. """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes = [IsAuthenticated]

    # @api_view(['POST'])
    # def post(self, ):


# View for registering new user
class CreateMessageView(generics.CreateAPIView):
    """ API endpoint for creating new messages. """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateMessageSerializer


class GetLikeCountView(generics.ListAPIView):
    """ API endpoint for liking a messages. """
    permission_classes = (IsAuthenticated,)
    serializer_class = GetLikeCountSerializer

    def get_queryset(self):
        # message_id = self.kwargs.get('pk')
        # try:
        message = Message.objects.filter(id=self.kwargs.get('pk'))

        # except message.count() < 1:     # TODO Raise exception when no message exists
        #     raise NotFound()
        return message


class GetCoordinatesView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetCoordinatesSerializer

    def get_queryset(self):
        message = Message.objects.filter(id=self.kwargs.get('pk'))
        return message


