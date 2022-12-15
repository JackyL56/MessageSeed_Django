from django.db import models
from django.contrib.auth.models import User
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
        help_text='The highest score out of all messages this author has posted.')

    # Metadata
    class Meta:
        ordering = ['high_score', 'username']
        app_label = 'database'

    # Methods
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
    number_likes = models.IntegerField(
        default=0,
        verbose_name='Number of Likes',
        help_text='Number of times this seedling got watered.')

    # Metadata
    class Meta:
        ordering = ['-postdate', 'author']
        app_label = 'database'

    # Methods
    def __str__(self):
        return '%s by %s' % (self.title, self.author.__str__())

