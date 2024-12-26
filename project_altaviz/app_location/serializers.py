from rest_framework import serializers
from .models import *
from app_bank.serializers import BankSerializer, StateNoRegionSerializer
# from app_custodian.models import Branch
# from app_custodian.serializers import BranchListSerializer
# from app_users.serializers import RegionAloneSerializer

# Create your serializers here.
class LocationSerializer(serializers.ModelSerializer):
	region = serializers.SerializerMethodField()
	class Meta:
		model = Location
		fields = [ 'id', 'location', 'region',]
	def get_region(self, obj): # get_region: syntax: get_<fieldname>, obj is the location instance from view logic
		from app_users.serializers import RegionAloneSerializer
		# print(f'obj ##########: {obj}')
		# print(f'obj.region ##########: {obj.region}')
		return RegionAloneSerializer(obj.region).data  # Serialize and return the region data

class LocationNoRegionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Location
		fields = [ 'id', 'location',]

class LocationAloneSerializer(serializers.ModelSerializer):
	class Meta:
		model = Location
		fields = [ 'id', 'location', ]

class JustLocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Location
		fields = [ 'location', ]

class LocationWithStateAndBankSerializer(serializers.ModelSerializer):
	state = StateNoRegionSerializer()
	# bank = BankSerializer()
	class Meta:
		model = Location
		fields = [ 'id', 'location', 'state']

class LocationBranches(serializers.ModelSerializer):
	branches = serializers.SerializerMethodField()
	class Meta:
		model = Location
		fields = [ 'id', 'location', 'branches']

	def get_branches(self, instance):
		from app_custodian.serializers import BranchListSerializer
		branches = instance.locationbranches.all()
		return BranchListSerializer(branches, many=True).data
