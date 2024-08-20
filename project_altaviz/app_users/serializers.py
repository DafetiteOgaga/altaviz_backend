from rest_framework import serializers
from .models import *
from app_bank.serializers import CustodianSerializer

# Create your serializers here.
class UserCreateUpdateSerializer(serializers.ModelSerializer):
	department = serializers.SlugRelatedField(
		queryset=Department.objects.all(), slug_field='name'
	)
	password = serializers.CharField(write_only=True)
	# custodian = CustodianSerializer(source='mail', read_only=True)
	class Meta:
		model = User
		fields = (
			'id', 'first_name', 'last_name', 'middle_name',
			'username', 'email', 'phone', 'wphone', 'address',
			'department', 'deliveries', 'profile_picture', 'aboutme',
			'pendings', 'is_deleted',
			'password', # for hashing during user creation
			# 'custodian',
		)
	def create(self, validated_data):
		department = validated_data.pop('department') # get the department
		email = validated_data.pop('email')
		username = validated_data.pop('username')
		password = validated_data.pop('password')
		user = User.objects.create_user( # for hashing during user creation
			email=email,
			username=username,
			password=password,
			department=department,
			**validated_data  # other fields
		)
		return user

	def get_profile_picture(self, obj):
		request = self.context.get('request')
		if obj.profile_picture:
			return request.build_absolute_uri(obj.profile_picture.url)
		return None

class UserReadSerializer(serializers.ModelSerializer):
	department = serializers.SlugRelatedField(
		queryset=Department.objects.all(), slug_field='name'
	)
	# password = serializers.CharField(write_only=True)
	custodian = CustodianSerializer(source='mail', read_only=True)
	class Meta:
		model = User
		fields = (
			'id', 'first_name', 'last_name', 'middle_name',
			'username', 'email', 'phone', 'wphone', 'address',
			'department', 'deliveries', 'profile_picture', 'aboutme',
			'pendings', 'is_deleted',
			# 'password', # for hashing during user creation
			'custodian',
		)
	# def create(self, validated_data):
	# 	department = validated_data.pop('department') # get the department
	# 	email = validated_data.pop('email')
	# 	username = validated_data.pop('username')
	# 	password = validated_data.pop('password')
	# 	user = User.objects.create_user( # for hashing during user creation
	# 		email=email,
	# 		username=username,
	# 		password=password,
	# 		department=department,
	# 		**validated_data  # other fields
	# 	)
	# 	return user

	# def get_profile_picture(self, obj):
	# 	request = self.context.get('request')
	# 	if obj.profile_picture:
	# 		return request.build_absolute_uri(obj.profile_picture.url)
	# 	return None


# # original serializer
# class UserSerializer(serializers.ModelSerializer):
# 	department = serializers.SlugRelatedField(
# 		queryset=Department.objects.all(), slug_field='name'
# 	)
# 	password = serializers.CharField(write_only=True)
# 	custodian = CustodianSerializer(source='mail', read_only=True)
# 	class Meta:
# 		model = User
# 		fields = (
# 			'id', 'first_name', 'last_name', 'middle_name',
# 			'username', 'email', 'phone', 'wphone', 'address',
# 			'department', 'deliveries', 'profile_picture', 'aboutme',
# 			'pendings', 'is_deleted',
# 			'password', # for hashing during user creation
# 			'custodian',
# 		)
# 	def create(self, validated_data):
# 		department = validated_data.pop('department') # get the department
# 		email = validated_data.pop('email')
# 		username = validated_data.pop('username')
# 		password = validated_data.pop('password')
# 		user = User.objects.create_user( # for hashing during user creation
# 			email=email,
# 			username=username,
# 			password=password,
# 			department=department,
# 			**validated_data  # other fields
# 		)
# 		return user

# 	def get_profile_picture(self, obj):
# 		request = self.context.get('request')
# 		if obj.profile_picture:
# 			return request.build_absolute_uri(obj.profile_picture.url)
# 		return None






# # ###################################################
# class UserSerializer(serializers.ModelSerializer):
#     department = serializers.SlugRelatedField(
#         queryset=Department.objects.all(), slug_field='name'
#     )
#     custodian = CustodianSerializer()

#     class Meta:
#         model = User
#         fields = (
#             'id', 'first_name', 'last_name', 'middle_name',
#             'username', 'email', 'phone', 'wphone', 'address',
#             'department', 'deliveries', 'profile_picture', 'aboutme',
#             'pendings', 'is_deleted', 'password', 'custodian'
#         )
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }

#     def create(self, validated_data):
#         custodian_data = validated_data.pop('custodian')
#         department = validated_data.pop('department')
        
#         # Create the user
#         user = User.objects.create_user(
#             department=department,
#             **validated_data
#         )

#         # Handle the Custodian and Bank creation
#         bank_data = custodian_data.pop('bank')
#         bank, created = Bank.objects.get_or_create(**bank_data)

#         Custodian.objects.create(
#             email=user,
#             bank=bank,
#             **custodian_data
#         )

#         return user

#     def update(self, instance, validated_data):
#         custodian_data = validated_data.pop('custodian', None)
#         department = validated_data.pop('department', None)
        
#         # Update user fields
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
        
#         # Update the Custodian and Bank if needed
#         if custodian_data:
#             bank_data = custodian_data.pop('bank')
#             bank, created = Bank.objects.get_or_create(**bank_data)
            
#             custodian = instance.mail  # related_name 'mail' used in Custodian model
#             custodian.bank = bank
#             for attr, value in custodian_data.items():
#                 setattr(custodian, attr, value)
#             custodian.save()

#         instance.save()
#         return instance

# # valid data structure
# {
#   "first_name": "John",
#   "last_name": "Doe",
#   "middle_name": "Smith",
#   "username": "johndoe",
#   "email": "johndoe@example.com",
#   "phone": "1234567890",
#   "wphone": "0987654321",
#   "address": "123 Main Street",
#   "department": "IT",
#   "deliveries": 10,
#   "profile_picture": null,
#   "aboutme": "I love coding!",
#   "pendings": 2,
#   "password": "strongpassword",
#   "custodian": {
#     "state": "Lagos",
#     "branch": "Ikeja",
#     "location": "Allen Avenue",
#     "bank": {
#       "name": "Zenith Bank"
#     }
#   }
# }
