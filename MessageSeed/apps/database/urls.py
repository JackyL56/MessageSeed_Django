from django.urls import path
from apps.database.views import *

urlpatterns = [
    path('message/create/', CreateMessageView.as_view(), name='api_create_message'),
    path('message/<int:pk>/like_count/', GetLikeCountView.as_view(), name='api_get_like_count'),
    path('message/<int:pk>/coordinates/', GetCoordinatesView.as_view(), name='api_get_coordinates')
]
