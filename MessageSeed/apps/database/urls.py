from django.urls import path
from apps.database.views import *

urlpatterns = [
    path('message/create/', CreateMessageView.as_view(), name='api_create_message'),
    path('message/<int:pk>/', GetMessageView.as_view(), name='api_get_message'),
    path('message/<int:pk>/like_count/', GetLikeCountView.as_view(), name='api_get_like_count'),
    path('message/<int:pk>/coordinates/', GetCoordinatesView.as_view(), name='api_get_coordinates'),
    path('message/<int:pk>/like/', LikeMessageView.as_view(), name='api_like_message'),
    path('message/<int:pk>/unlike/', UnlikeMessageView.as_view(), name='api_unlike_message'),

    path('profile/', ProfileView.as_view(), name='api_my_profile'),
    path('profile/messages/', MyMessagesView.as_view(), name='api_my_messages'),
    path('profile/liked_messages/', MyLikedMessagesView.as_view(), name='api_my_liked_messages'),
    path('profile/<int:pk>/', GetAuthorView.as_view(), name='api_get_author'),


]
