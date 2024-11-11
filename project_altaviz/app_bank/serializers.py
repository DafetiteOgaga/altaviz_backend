from rest_framework import serializers
from .models import *
from app_location.models import Location
from app_custodian.models import Branch
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your serializers here.
class StateSerializer(serializers.ModelSerializer):
	class Meta:
		model = State
		fields = '__all__'

class StateNoRegionSerializer(serializers.ModelSerializer):
	class Meta:
		model = State
		fields = ['id', 'name', 'initial']

class BankSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bank
		fields = ['id', 'name',]
