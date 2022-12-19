from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Author(models.Model):

    # Fields
    username = models.OneToOneField(
                User,
                on_delete=models.CASCADE,
                related_name='author',
                primary_key=True)
    high_score = models.IntegerField(
                default=0,
                help_text='The highest score out of all messages this author has posted.') # TODO Set high score of author automatically

    # Metadata
    class Meta:
        ordering = ['high_score', 'username']
        app_label = 'database'
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('author-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.username.__str__()


class Message(models.Model):

    # Fields

    title = models.CharField(
        verbose_name='Title',
        max_length=42,
        help_text='Title for the message.')
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='messages',
        related_query_name='message',
        help_text='Author of the message.')
    message = models.TextField(
        max_length=500,
        help_text='Contains the message.')
    postdate = models.DateTimeField(
        auto_now=True,
        verbose_name='The date of the message when it was posted.')
    user_likes = models.ManyToManyField(
        User,
        blank=True,
        related_name='user_likes',
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
        ordering = ['-postdate', 'author']
        app_label = 'database'
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    # Properties
    @property
    def like_count(self):
        return self.user_likes.count()

    # @property
    # def get_coordinates(self):
    #     return self.latitude, self.longitude

    # Methods
    def __str__(self):
        return '%s by %s' % (self.title, self.author.__str__())

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('message-detail-view', args=[str(self.id)])

