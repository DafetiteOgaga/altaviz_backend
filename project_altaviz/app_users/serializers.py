from rest_framework import serializers
from .models import *
from app_custodian.models import Branch
from app_custodian.serializers import CustodianSerializer, BranchSerializer
from app_location.serializers import LocationSerializer, LocationAloneSerializer, LocationWithStateAndBankSerializer
from app_bank.serializers import StateSerializer
from app_deliveries.serializers import ReadUserDeliveriresSerializer

# Create your serializers here.
class UserSummarizedDetailsSerializer(serializers.ModelSerializer):
	location = LocationAloneSerializer()
	state = StateSerializer()
	region = serializers.SlugRelatedField(
		queryset=Region.objects.all(), slug_field='name'
	)
	class Meta:
		model = User
		fields = [
			'id', 'first_name', 'last_name', 'email', 'phone', 'wphone',
			'username', 'gender', 'role', 'region', 'state', 'location'
			]

class UserMiniDetailsSerializer(serializers.ModelSerializer):
	state = StateSerializer()
	class Meta:
		model = User
		fields = [
			'id', 'email', 'first_name', 'last_name',
			'username', 'role', 'state'
			]

class RegionReadSerializer(serializers.ModelSerializer):
	helpdesk = UserSummarizedDetailsSerializer(read_only=True)
	supervisor = UserSummarizedDetailsSerializer(read_only=True)
	class Meta:
		model = Region
		fields = '__all__'

class UserReadSerializer(serializers.ModelSerializer):
	# profile_picture = serializers.SerializerMethodField()
	# custodian = CustodianSerializer(read_only=True) # Access custodian
	# custodian = serializers.SerializerMethodField()
	branch = serializers.SerializerMethodField()
	# branch = BranchSerializer(source='branchcustodian', read_only=True) # Access branch through custodian
	location = LocationSerializer(read_only=True)
	state = StateSerializer()
	region = RegionReadSerializer(read_only=True)
	userRegion = serializers.SlugRelatedField(
		queryset=Region.objects.all(), slug_field='name',
		source='region'
	)
	deliveryPoints = ReadUserDeliveriresSerializer(source='userdeliveries')
	class Meta:
		model = User
		fields = (
			'id', 'first_name', 'last_name', 'middle_name', 'gender', 'dob',
			'username', 'email', 'phone', 'wphone', 'address', 'role',
			'region', 'userRegion', 'location', 'deliveryPoints', 'profile_picture', 'aboutme',
			'pendings', 'is_deleted', 'branch', 'state', #, 'location', 'state', 'branch', 'custodian',
		)
	# def get_custodian(self, obj):
	# 	# custodian = obj.custodiandata.first()
	# 	# if custodian:
	# 	# 	return CustodianSerializer(custodian).data
	# 	# return None
	# 	return CustodianSerializer(obj.custodiandata.first()).data
	def get_branch(self, obj):
		# print(f'obj (brSer) ###### : {obj}')
		# print(f'obj.branchcustodian b>c (brSer) ###### : {obj.branchcustodian.all()}')
		# print(f'obj.branchcustodian user->custodian->branch (brSer) ###### : {obj.custodiandata.all().first().branch}')
		# branchSerializer = obj.custodiandata.all().first().branch
		branchSerializer = obj.custodiandata.all().first()
		print(f'branchSerializer ###### : {branchSerializer}')
		if branchSerializer:
			# custodian branch
			text = 'CUSTODIAN branch'
			branchSerializer = obj.custodiandata.all().first().branch
		else:
			# random branch for general users
			text = 'RANDOM branch for general users'
			branchSerializer = Branch.objects.filter(region=obj.region).first()
		print(f'branchSerializer ({text}) ###### : {branchSerializer}')
		# print(f'obj.branchcustodian.first() (brSer) ###### : {obj.branchcustodian.first()}')
		return BranchSerializer(branchSerializer).data
		# else:
		# 	print(f'user region: {obj.region}')
		# 	randomBranch = Branch.objects.filter(region=obj.region).first()
		# 	print(f'random branch: {randomBranch}')
		# 	return BranchSerializer(randomBranch).data

class UserCreateSerializer(serializers.ModelSerializer):
	location = serializers.PrimaryKeyRelatedField(
		queryset=Location.objects.all()
	)
	state = serializers.SlugRelatedField(
		queryset=State.objects.all(), slug_field='name'
	)
	region = serializers.SlugRelatedField(
		queryset=Region.objects.all(), slug_field='name'
	)
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = (
			'id', 'first_name', 'last_name', 'middle_name',
			'username', 'email', 'phone', 'wphone', 'address',
			'region', 'role', 'profile_picture',
			'aboutme', 'pendings', 'is_deleted', 'location',
			'state', 'gender', 'dob',
			'password', # for hashing during user creation
		)
	def create(self, validated_data):
		# Location = validated_data.pop('Location')
		email = validated_data.pop('email')
		username = validated_data.pop('username')
		password = validated_data.pop('password')
		user = User.objects.create_user( # for hashing during user creation
			email=email,
			username=username,
			password=password,
			# Location=Location  # dynamically assign the Location using the stored model
			**validated_data  # other fields
		)
		return user

	def get_profile_picture(self, obj):
		request = self.context.get('request')
		if obj.profile_picture:
			return request.build_absolute_uri(obj.profile_picture.url)
		return None

# use RegionReadSerializer here instaed
class UserReadHandlersSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'id', 'first_name', 'last_name', 'username',
			'email', # 'Location', 'aboutme', 'profile_picture',
			'phone', 'wphone', 'role',
		)

class UserUpdateDetailsSerializer(serializers.ModelSerializer):
	custodian = CustodianSerializer(read_only=True)
	class Meta:
		model = User
		fields = (
			'id', 'first_name', 'last_name', 'middle_name',
			'phone', 'wphone',
			'role',
			# 'Location',
			'profile_picture', 'aboutme',
			'custodian',
		)

class RegionAloneSerializer(serializers.ModelSerializer):
	class Meta:
		model = Region
		fields = ['id', 'name',]

class EngineerSerializer(serializers.ModelSerializer):
	engineer = UserSummarizedDetailsSerializer()
	# location = serializers.SlugRelatedField(
	# 	queryset=Location.objects.all(), slug_field='location'
	# )
	class Meta:
		model = Engineer
		fields = ['id', 'engineer']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EngineerAssignmentNotificaionSerializer(serializers.ModelSerializer):
    supervisor = UserMiniDetailsSerializer()
    location = LocationWithStateAndBankSerializer()
    class Meta:
        model = EngineerAssignmentNotificaion
        fields = '__all__'

class PatchEngineerAssignmentNotificaionSerializer(serializers.ModelSerializer):
    supervisor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    class Meta:
        model = EngineerAssignmentNotificaion
        fields = '__all__'

class UserUpdateSerializer(serializers.ModelSerializer):
	location = serializers.SlugRelatedField(
		queryset=Location.objects.all(), slug_field='location'
	)
	state = serializers.SlugRelatedField(
		queryset=State.objects.all(), slug_field='name'
	)
	region = serializers.SlugRelatedField(
		queryset=Region.objects.all(), slug_field='name'
	)
	# password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = '__all__'
			# 'password', # for hashing during user creation

	def get_profile_picture(self, obj):
		request = self.context.get('request')
		if obj.profile_picture:
			return request.build_absolute_uri(obj.profile_picture.url)
		return None

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

class UpdateLocationAndBranchNotificationSerializer(serializers.ModelSerializer):
    requestUser = UserSummarizedDetailsSerializer()
    class Meta:
        model = UpdateLocationAndBranchNotification
        fields = '__all__'

class AllUsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active', 'profile_picture']

class UserNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name']