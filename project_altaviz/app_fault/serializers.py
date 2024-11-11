from rest_framework import serializers
from .models import *
from app_location.serializers import LocationSerializer
from app_users.serializers import UserReadHandlersSerializer, UserSummarizedDetailsSerializer
# from app_help_desk.serializers import HelpDeskSerializer
# from app_supervisor.serializers import SupervisorSerializer
from app_custodian.serializers import CustodianSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your serializers here.
class FaultNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultName
        fields = ['id', 'name',]

class FaultCreateUpdateSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        queryset=FaultName.objects.all()
    )
    logged_by = serializers.SlugRelatedField(
        slug_field='custodian__email',
        queryset=Custodian.objects.all()
    )
    assigned_to = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all()
    )
    managed_by = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all()
    )
    supervised_by = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all()
    )
    # location = serializers.SlugRelatedField(
    #     slug_field='location',
    #     queryset=Location.objects.all()
    # )
    class Meta:
        model = Fault
        fields = '__all__'

class FaultReadSerializer(serializers.ModelSerializer):
    title = FaultNameSerializer()
    location = LocationSerializer()
    assigned_to = UserSummarizedDetailsSerializer()
    managed_by = UserSummarizedDetailsSerializer()
    supervised_by = UserSummarizedDetailsSerializer()
    logged_by = CustodianSerializer()
    replacement_engineer=UserSummarizedDetailsSerializer()
    confirmed_by = UserSummarizedDetailsSerializer()
    class Meta:
        model = Fault
        fields = '__all__'

class FaultConfirmResolutionSerializer(serializers.ModelSerializer):
    # confirmed_by = serializers.SlugRelatedField(
	# 	queryset=User.objects.all(), slug_field='email'
	# )
    class Meta:
        model = Fault
        fields = ['confirmed_by', 'confirm_resolve']

class FaultPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fault
        fields = ['confirmed_by', 'confirm_resolve', 'verify_resolve']
