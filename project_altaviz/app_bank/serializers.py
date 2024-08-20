from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your serializers here.
class BankSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bank
		fields = ['id', 'name',]

class CustodianSerializer(serializers.ModelSerializer):
	bank = serializers.SlugRelatedField(
		queryset=Bank.objects.all(), slug_field='name'
	)
	email = serializers.SlugRelatedField(
		queryset=User.objects.all(), slug_field='email'
	)
	class Meta:
		model = Custodian
		fields = ['id', 'email', 'bank', 'state', 'branch', 'location',]
	# def create(self, validated_data):
	# 	bank = validated_data.pop('bank') # get the bank)
	# 	email = validated_data.pop('email') # get the user email)
	# 	custodian = Custodian.objects.create(
	# 		bank=bank,
	# 		email=email,
	# 		**validated_data  # other fields
	# 	)
	# 	return custodian