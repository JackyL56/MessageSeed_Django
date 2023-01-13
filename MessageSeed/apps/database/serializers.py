import datetime

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from django.db.models import Count
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
################################### GLOBALS ############################################



########################################################################################

class CreateMessageSerializer(serializers.ModelSerializer):
    """ Serializer to create a Message """
    unix_post_date = serializers.SerializerMethodField(read_only=True)
    unix_death_date = serializers.SerializerMethodField(read_only=True) ## FIXME read_only may be false?

    def get_unix_post_date(self, obj):
        return timezone.now().timestamp() * 1000

    def get_unix_death_date(self, obj):
        return (timezone.now()+timedelta(days=Helper.DEFAULT_LIFETIME)).timestamp() * 1000

    class Meta:
        model = Message
        fields = ['id', 'title', 'author', 'message', 'state', 'unix_post_date',
                  'unix_death_date', 'user_likes', 'latitude', 'longitude']

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
            death_date=(timezone.now()+timedelta(days=Helper.DEFAULT_LIFETIME))
        )
        message.save()

        author.add_experience(Helper.EXPERIENCE_CREATED_MESSAGE)

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


def get_most_liked_message(obj):
    """ Helper Function to get the most liked message of an author. """
    messages = obj.messages.all()
    most_liked_message = messages.first()
    count = most_liked_message.user_likes.count()
    for m in messages:
        if m.user_likes.count() > count:
            most_liked_message = m
            count = most_liked_message.user_likes.count()
    return most_liked_message


class GetAuthorSerializer(serializers.ModelSerializer):
    """ Serializer to get a specific Author """
    author_name = serializers.CharField()
    likes_received_total = serializers.SerializerMethodField(read_only=True)
    likes_given_total = serializers.SerializerMethodField(read_only=True)

    level = serializers.FloatField()
    experience_next = serializers.FloatField()
    experience_previous = serializers.FloatField()

    most_liked_message_count = serializers.SerializerMethodField(read_only=True)
    most_liked_message_id = serializers.SerializerMethodField(read_only=True)

    def get_likes_received_total(self, obj):
        return obj.messages.all().aggregate(Count('user_likes'))['user_likes__count']

    def get_likes_given_total(self, obj):
        return obj.messages_liked.count()

    def get_most_liked_message_count(self, obj):
        return get_most_liked_message(obj).user_likes.count()

    def get_most_liked_message_id(self, obj):
        return get_most_liked_message(obj).id

    class Meta:
        model = Author
        fields = ['user_id', 'author_name', 'level', 'experience', 'experience_next', 'experience_previous', 'likes_received_total',  # 'messages', 'liked_messages',
                  'likes_given_total', 'most_liked_message_count', 'most_liked_message_id']


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
        return GetMessageSerializer(obj.messages.all(), many=True, read_only=True, context=self.context).data

    class Meta:
        model = Author
        fields = ['user_id', 'my_messages']


class GetMyLikedMessagesSerializer(serializers.ModelSerializer):
    """ Serializer to get all Messages of the current user. """
    liked_messages = serializers.SerializerMethodField(read_only=True)

    def get_liked_messages(self, obj):
        return GetMessageSerializer(obj.messages_liked.all(), many=True, read_only=True, context=self.context).data

    class Meta:
        model = Author
        fields = ['user_id', 'liked_messages']
