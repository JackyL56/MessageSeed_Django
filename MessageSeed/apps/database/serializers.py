import datetime

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

from datetime import timedelta
from django.utils import timezone

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
        fields = ['id', 'author', 'latitude', 'longitude']


########################################################################################
########################################################################################

class CreateMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['url', 'id', 'title', 'author', 'message', 'post_date',
                  'death_date', 'user_likes', 'latitude', 'longitude']

    # Methods
    def create(self, validated_data):
        message = Message.objects.create(
            title=validated_data['title'],
            author=validated_data['author'],
            message=validated_data['message'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            death_date=(timezone.now()+timedelta(days=7))  # TODO Rn, default death date is after a week
        )
        message.save()

        return message


class GetMessageSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField()
    unix_post_date = serializers.FloatField()
    unix_death_date = serializers.FloatField()

    class Meta:
        model = Message
        fields = ['id', 'title', 'author', 'message', 'unix_post_date', 'unix_death_date',
                  'user_likes', 'like_count', 'latitude', 'longitude']

    # def to_representation(self, instance):
    #     self.fields['post_date'] = instance.post_date.timestamp()*1000
    #     self.fields['death_date'] = instance.death_date.timestamp()*1000
    #
    #     # formatted_death_date = instance.death_date.timestamp()*1000
    #
    #     return super().to_representation(instance)


class GetLikeCountSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField()

    class Meta:
        model = Message
        fields = ['id', 'like_count']


class GetCoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'latitude', 'longitude']

