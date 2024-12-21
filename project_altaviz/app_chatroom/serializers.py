from rest_framework import serializers
from .models import *
from app_users.serializers import UserNamesSerializer

# Create your serializers here.
class ChatsSerializer(serializers.ModelSerializer):
    user = UserNamesSerializer(read_only=True)
    contact = UserNamesSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'user', 'contact', 'message', 'timestamp']
        read_only_fields = ['timestamp']