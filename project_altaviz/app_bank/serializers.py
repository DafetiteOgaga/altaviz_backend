from rest_framework import serializers
from .models import *
from app_location.models import Location
from app_custodian.models import Branch
# from app_custodian.serializers import BranchListSerializer
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

class BankBranchSerializer(serializers.ModelSerializer):
	locations = serializers.SerializerMethodField()
	class Meta:
		model = Bank
		fields = ['id', 'name', 'locations']

	def get_locations(self, instance):
		# Lazy import inside the method
		from app_location.serializers import LocationBranches
		locations = instance.banklocations.all()
		return LocationBranches(locations, many=True).data
