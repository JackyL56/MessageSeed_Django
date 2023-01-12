import datetime

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from django.db.models import Sum, Count
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
    user = serializers.HyperlinkedRelatedField(view_name='author-detail', queryset=Author.objects.all())

    class Meta:
        model = Author
        fields = ['url', 'user', 'high_score']


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    # author = serializers.HyperlinkedRelatedField(view_name='message-detail', queryset=Message.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'author', 'state', 'latitude', 'longitude', 'user_likes']


########################################################################################
########################################################################################

class CreateMessageSerializer(serializers.ModelSerializer):
    """ Serializer to create a Message """
    class Meta:
        model = Message
        fields = ['id', 'title', 'author', 'message', 'state', 'post_date',
                  'death_date', 'user_likes', 'latitude', 'longitude']

    # Methods
    def create(self, validated_data):
        author = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            author = request.user.author

        message = Message.objects.create(
            title=validated_data['title'],
            author=author,
            message=validated_data['message'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            death_date=(timezone.now()+timedelta(days=7))  # TODO Rn, default death date is after a week
        )
        message.save()

        return message


class GetMessageSerializer(serializers.ModelSerializer):
    """ Serializer to get a specific Message """
    like_count = serializers.IntegerField()
    unix_post_date = serializers.FloatField()
    unix_death_date = serializers.FloatField()
    author_name = serializers.SerializerMethodField(read_only=True)
    me_liked = serializers.SerializerMethodField(read_only=True)

    def get_author_name(self, obj):
        return obj.author.user.username

    def get_me_liked(self, obj):
        """ Returns a true if the current user already likes the message."""
        user = self.context['request'].user.id
        if obj.user_likes.all().filter(user=user).exists():
            return True
        return False

        # if user in obj.user_likes.all():
        #     return True
        # else:
        #     return False

    class Meta:
        model = Message
        fields = ['id', 'title', 'author', 'author_name', 'message', 'state', 'unix_post_date', 'unix_death_date',
                  'user_likes', 'like_count', 'latitude', 'longitude', 'me_liked']


class GetAuthorSerializer(serializers.ModelSerializer):
    """ Serializer to get a specific Author """
    author_name = serializers.CharField()
    liked_messages = serializers.SerializerMethodField(read_only=True)
    likes_received_total = serializers.SerializerMethodField(read_only=True)
    likes_given_total = serializers.SerializerMethodField(read_only=True)

    def get_liked_messages(self, obj):
        return obj.messages_liked.values()

    def get_likes_received_total(self, obj):
        return obj.messages.all().aggregate(Count('user_likes'))['user_likes__count']

    def get_likes_given_total(self, obj):
        return obj.messages_liked.count()

    class Meta:
        model = Author
        fields = ['user_id', 'author_name', 'level', 'experience', 'messages', 'liked_messages', 'likes_received_total',
                  'likes_given_total']


## FIXME May not be needed
class GetLikeCountSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField()

    class Meta:
        model = Message
        fields = ['id', 'like_count']


class GetCoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'latitude', 'longitude']


class GetMyMessagesSerializer(serializers.ModelSerializer):
    """ Serializer to get all Messages of the current user. """
    my_messages = serializers.SerializerMethodField(read_only=True)

    def get_my_messages(self, obj):
        return obj.messages.values()

    class Meta:
        model = Author          ## TODO LIST DOES NOT CONTAIN THE PROPERTIES
        fields = ['user_id', 'my_messages'] # 'messages' for only the id's
