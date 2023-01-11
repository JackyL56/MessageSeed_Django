from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
# Create your models here.


class Author(models.Model):

    # Fields
    user = models.OneToOneField(
                User,
                on_delete=models.CASCADE,
                related_name='author',
                primary_key=True)
    high_score = models.IntegerField(
                default=0,
                help_text='The highest score out of all messages this author has posted.') # TODO Set high score of author automatically
    level = models.IntegerField(
                default=0,
                help_text='Level of the author.')
    experience = models.IntegerField(
                default=0,
                help_text='Current Experience points of the author.')

    # Metadata
    class Meta:
        ordering = ['high_score', 'user']
        app_label = 'database'
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    @property
    def get_username(self):
        return self.__str__()

    @property
    def get_liked_messages_count(self):
        return self.messages_liked.count()

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('author-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.user.__str__()


class Message(models.Model):

    # Fields

    title = models.CharField(
        verbose_name='Title',
        max_length=42,
        help_text='Title for the message.')
    author = models.ForeignKey(
        Author,
        blank=True,
        on_delete=models.CASCADE,
        related_name='messages',
        related_query_name='message',
        help_text='Author of the message.')
    message = models.TextField(
        max_length=500,
        help_text='Contains the message.')
    # post_time = models.DecimalField(
    #     default=Decimal(datetime.now().timestamp()*1000),  # Epoch Unix Representation of datetime (in ms)
    #     max_digits=20,
    #     decimal_places=3,
    #     verbose_name='Time of Death for the message.'
    # )
    # death_time = models.DecimalField(
    #     default=Decimal((datetime.now()+timedelta(days=7)).timestamp()*1000),   # Default time till death: 7 days after posting
    #     max_digits=20,
    #     decimal_places=3,
    #     verbose_name='Time of Death for the message.'
    # )
    post_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='The date of the message when it was posted.')
    death_date = models.DateTimeField(
        blank=True,
        verbose_name='Time of Death for the message.'
    )
    user_likes = models.ManyToManyField(
        Author,
        blank=True,
        related_name='messages_liked',
        help_text='List of Users who have liked this message.')
    latitude = models.DecimalField(
        max_digits=18,
        decimal_places=15,
        help_text='Latitude of the location at which this message was posted.')
    longitude = models.DecimalField(
        max_digits=18,
        decimal_places=15,
        help_text='Longitude of the location at which this message was posted.')

    # Metadata
    class Meta:
        ordering = ['post_date', 'author']
        app_label = 'database'
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    # Properties
    @property
    def like_count(self):
        return self.user_likes.count()

        # Time of post and death dates in unix epochs (milliseconds)
    @property
    def unix_post_date(self):
        return self.post_date.timestamp()*1000

    @property
    def unix_death_date(self):
        return self.death_date.timestamp()*1000

    @property
    def user_like_list(self):
        return self.user_likes

    # Methods
    def __str__(self):
        return '%s by %s' % (self.title, self.author.__str__())

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('message-detail-view', args=[str(self.id)])
