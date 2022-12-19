from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

#######################################################################################
#                                  ADMIN VIEW                                         #
#######################################################################################
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.HyperlinkedRelatedField(view_name='author-detail', queryset=Author.objects.all())

    class Meta:
        model = Author
        fields = ['url', 'username', 'high_score']


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    # author = serializers.HyperlinkedRelatedField(view_name='message-detail', queryset=Message.objects.all())

    class Meta:
        model = Message
        fields = ['url', 'id', 'title', 'author', 'message', 'postdate', 'user_likes', 'latitude', 'longitude']


########################################################################################
########################################################################################

class CreateMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['url', 'id', 'title', 'author', 'message', 'postdate', 'user_likes', 'latitude', 'longitude']

    # Methods
    def create(self, validated_data):
        message = Message.objects.create(
            title=validated_data['title'],
            author=validated_data['author'],
            message=validated_data['message'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude']
            # postdate=validated_data['postdate']
        )
        message.save()

        return message


class GetLikeCountSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField()

    class Meta:
        model = Message
        fields = ['id', 'like_count']


class GetCoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'latitude', 'longitude']


class LikeMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'author', 'like_count']

    def update(self, instance, validated_data):
        authors = validated_data.pop('author')
        instance = super()

