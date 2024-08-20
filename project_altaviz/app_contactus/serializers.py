from rest_framework import serializers
from .models import *

# Create your serializers here.
class ContactUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'message']
