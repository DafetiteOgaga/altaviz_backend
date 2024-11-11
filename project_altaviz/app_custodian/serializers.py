from rest_framework import serializers
from .models import *
from app_bank.serializers import BankSerializer, StateNoRegionSerializer
# from app_users.serializers import EngineerSerializer
from app_location.serializers import LocationSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your serializers here.
# class CustodianCreateUpdateSerializer(serializers.ModelSerializer):
# 	custodian = serializers.SlugRelatedField(
# 		queryset=User.objects.all(), slug_field='email'
# 	)
# 	class Meta:
# 		model = Custodian
# 		fields = '__all__'

class CustodianSerializer(serializers.ModelSerializer):
	# custodian = serializers.SerializerMethodField()
	# custodian = serializers.EmailField(source='custodian.email', read_only=True)
	branch = serializers.SerializerMethodField()
	class Meta:
		model = Custodian
		fields = ['id', 'branch']
		# fields = '__all__'
	# def get_custodian(self, instance):
	# 	# Lazy import inside the method
	# 	print(f'instance.custodian ##########: {instance}')
	# 	print(f'instance.custodian ##########: {instance.custodian}')
	# 	# print(f'instance.custodian##########: {instance.email}')
	# 	from app_users.serializers import UserSummarizedDetailsSerializer
	# 	return UserSummarizedDetailsSerializer(instance.custodian).data
	def get_branch(self, instance):
		# Lazy import inside the method
		# print(f'instance (branch) ##########: {instance}')
		# print(f'instance.custodian (branch) ##########: {instance.branch}')
		from .serializers import BranchSerializer
		return BranchSerializer(instance.branch).data

class CustodianGetUpdateCreateSerializer(serializers.ModelSerializer):
	custodian = serializers.SlugRelatedField(
		queryset=User.objects.all(), slug_field='custodian'
	)
	# branch = serializers.SlugRelatedField(
	# 	queryset=Branch.objects.all(), slug_field='name'
	# )
	class Meta:
		model = Custodian
		fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
	bank = BankSerializer(read_only=True)
	location = LocationSerializer(read_only=True)
	branch_engineer = serializers.SerializerMethodField()
	custodian = serializers.SerializerMethodField()
	state = StateNoRegionSerializer(read_only=True)
	region = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Branch
		fields = '__all__'
	def get_branch_engineer(self, instance):
		# Lazy import inside the method
		# print(f'eng instance (branch) ##########: {instance}')
		# print(f'eng instance.engineer (branch) ##########: {instance.branch_engineer}')
		from app_users.serializers import EngineerSerializer
		return EngineerSerializer(instance.branch_engineer).data
	def get_custodian(self, instance):
		# Lazy import inside the method
		# print(f'instance (branch) ##########: {instance}')
		# print(f'instance.custodian (branch) ##########: {instance.custodian}')
		from app_users.serializers import UserSummarizedDetailsSerializer
		return UserSummarizedDetailsSerializer(instance.custodian).data
	def get_region(self, instance):
		# Lazy import inside the method
		# print(f'region instance (branch) ##########: {instance}')
		# print(f'region instance.region (branch) ##########: {instance.region}')
		from app_users.serializers import RegionReadSerializer
		return RegionReadSerializer(instance.region).data
	# def get_engineer(self, instance):
	# 	# Lazy import inside the method
	# 	print(f'engineer instance (branch) ##########: {instance}')
	# 	print(f'engineer instance.custodian (branch) ##########: {instance.custodian}')
	# 	from app_users.serializers import UserSummarizedDetailsSerializer
	# 	return UserSummarizedDetailsSerializer(instance.engineer).data

class BranchListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Branch
		fields = ['id', 'name']

class JustBranchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Branch
		fields = ['name']

# class RequestDetailsChangeSerializer(serializers.ModelSerializer):
# 	custodian = serializers.SlugRelatedField(
# 		queryset=User.objects.all(), slug_field='email'
# 	)
# 	class Meta:
# 		model = RequestDetailsChange
# 		fields = [
# 			'id', 'custodian', 'state', 'branch',
# 			'location',
# 		]

# class RequestDetailsApproveSerializer(serializers.ModelSerializer):
# 	custodian = serializers.SlugRelatedField(
# 		queryset=User.objects.all(), slug_field='user'
# 	)
# 	class Meta:
# 		model = RequestDetailsChange
# 		fields = ['id', 'status', 'custodian',]

# class CustodianCreateUpdateSerializer(serializers.ModelSerializer):
# 	custodian = serializers.SlugRelatedField(
# 		queryset=User.objects.all(), slug_field='email'
# 	)
# 	branch = BranchSerializer()
# 	class Meta:
# 		model = Custodian
# 		fields = '__all__'
# class CustodianCreateUpdateSerializer(serializers.ModelSerializer):
# 	custodian = serializers.SlugRelatedField(
# 		queryset=User.objects.all(), slug_field='email'
# 	)
# 	branch = BranchSerializer()
# 	class Meta:
# 		model = Custodian
# 		fields = '__all__'
class CustodianCreateUpdateSerializer(serializers.ModelSerializer):
	custodian = serializers.SlugRelatedField(
		queryset=User.objects.all(), slug_field='email'
	)
	# branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())

	class Meta:
		model = Custodian
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Print the branch value received in the initial data
		if 'data' in kwargs:
			print(f'Branch data received before validation $$$$$: {kwargs["data"].get("branch")}')

	# def create(self, validated_data):
	# 	# Since the branch is passed as an object, no need to fetch or create it again
	# 	print(f'Creating custodian with branch: £££££ {validated_data["branch"]}')
	# 	# print(f'self: {self} £££££')
	# 	print(f'validated_data: {validated_data} £££££')
	# 	custodian = Custodian.objects.create(**validated_data)
	# 	print(f'cusodian: {custodian} £££££')
	# 	return custodian

	# def update(self, instance, validated_data):
	# 	# Since the branch is already an object, no extra logic needed
	# 	print(f'Updating custodian with branch £££££: {validated_data.get("branch")}')
	# 	# print(f'self: {self} £££££')
	# 	print(f'instance: {instance} £££££')
	# 	print(f'validated_data: {validated_data} £££££')
	# 	for attr, value in validated_data.items():
	# 		setattr(instance, attr, value)
		
	# 	instance.save()
	# 	return instance
	
	# def validate(self, data):
	# 	# Print the branch value received in the request data
	# 	print(f'Branch data received after validation $$$$$: {data.get("branch")}')
	# 	return data
	# def create(self, validated_data):
	# 	branch_data = validated_data.pop('branch')
	# 	print(f'in create method: branch is: {branch_data}')
	# 	branch, _ = Branch.objects.get_or_create(**branch_data)
	# 	print(f'get_or_create result: {branch_data}')
	# 	custodian = Custodian.objects.create(branch=branch, **validated_data)
	# 	print(f'custodian result: {custodian}')
	# 	return custodian

	# def update(self, instance, validated_data):
	# 	branch_data = validated_data.pop('branch', None)
	# 	print(f'in update method: branch: {branch_data}')
	# 	if branch_data:
	# 		branch, _ = Branch.objects.get_or_create(**branch_data)
	# 		print(f'get_or_create result: {branch}')
	# 		instance.branch = branch
	# 	for attr, value in validated_data.items():
	# 		setattr(instance, attr, value)
	# 	instance.save()
	# 	return instance