from django.contrib import admin
from .serializers import UserSerializer, GroupSerializer
from .models import Author, Message

# Register your models here.
admin.register(UserSerializer)
admin.register(GroupSerializer)

admin.site.register(Author)
admin.site.register(Message)
