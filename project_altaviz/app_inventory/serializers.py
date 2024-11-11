from rest_framework import serializers
from .models import *
from app_fault.models import Fault
from django.contrib.auth import get_user_model
User = get_user_model()
from app_users.serializers import UserReadHandlersSerializer, UserMiniDetailsSerializer
from app_fault.serializers import FaultReadSerializer
# from app_users.serializers import UserSerializer

# Create your serializers here.
class ComponentNameSerializer(serializers.ModelSerializer):
	class Meta:
		model = ComponentName
		fields = ['id', 'name']
		# fields = ['name', 'components', 'parts']

class ComponentSerializer(serializers.ModelSerializer):
	name = serializers.SlugRelatedField(
		queryset=ComponentName.objects.all(), slug_field='name')
	class Meta:
		model = Component
		fields = ['name', 'quantity',]

class PartNameSerializer(serializers.ModelSerializer):
	class Meta:
		model = PartName
		fields = ['id', 'name']
		# fields = ['name', 'components', 'parts']

class PartSerializer(serializers.ModelSerializer):
	name = serializers.SlugRelatedField(
		queryset=PartName.objects.all(), slug_field='name')
	class Meta:
		model = Part
		fields = ['name', 'quantity',]

# class RequestPartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RequestPart
#         fields = '__all__'

class RequestComponentCreateSerializer(serializers.ModelSerializer):
	name = serializers.SlugRelatedField(
		queryset=ComponentName.objects.all(), slug_field='name'
	)
	user = serializers.SlugRelatedField(
		queryset=User.objects.all(), slug_field='email'
	)
	fault = serializers.PrimaryKeyRelatedField(
		queryset=Fault.objects.all(),
		required=False, allow_null=True,
	)
	approved_by = serializers.SlugRelatedField(
		queryset=User.objects.all(), slug_field='email',
		required=False, allow_null=True,
	)
	class Meta:
		model = RequestComponent
		fields = '__all__'

class RequestComponentReadSerializer(serializers.ModelSerializer):
	name = ComponentNameSerializer()
	user = UserReadHandlersSerializer()
	fault = FaultReadSerializer()
	approved_by = UserReadHandlersSerializer()
	class Meta:
		model = RequestComponent
		fields = '__all__'

class RequestPartCreateSerializer(serializers.ModelSerializer):
	name = serializers.SlugRelatedField(
		queryset=PartName.objects.all(), slug_field='name'
	)
	user = serializers.SlugRelatedField(
		queryset=User.objects.all(), slug_field='email'
	)
	fault = serializers.PrimaryKeyRelatedField(
		queryset=Fault.objects.all(),
		required=False, allow_null=True,
	)
	approved_by = serializers.SlugRelatedField(
		queryset=User.objects.all(), slug_field='email',
		required=False, allow_null=True,
	)
	class Meta:
		model = RequestPart
		fields = '__all__'

class RequestPartReadSerializer(serializers.ModelSerializer):
	name = PartNameSerializer()
	user = UserReadHandlersSerializer()
	fault = FaultReadSerializer()
	approved_by = UserReadHandlersSerializer()
	class Meta:
		model = RequestPart
		fields = '__all__'

class UnconfirmedPartCreateSerializer(serializers.ModelSerializer):
	user = serializers.SlugRelatedField(
		queryset=User.objects.all(), slug_field='email'
	)
	approved_by = UserReadHandlersSerializer(required=False, allow_null=True)
	class Meta:
		model = UnconfirmedPart
		fields = '__all__'

class UnconfirmedPartSerializer(serializers.ModelSerializer):
	user = UserMiniDetailsSerializer(read_only=True)
	approved_by = UserReadHandlersSerializer(required=False, allow_null=True)
	class Meta:
		model = UnconfirmedPart
		fields = '__all__'

class RequestFaultComponentReadSerializer(serializers.ModelSerializer):
	name = ComponentNameSerializer()
	approved_by = UserReadHandlersSerializer()
	user = UserReadHandlersSerializer()
	fault = FaultReadSerializer()
	class Meta:
		model = RequestComponent
		fields = '__all__'

class RequestFaultPartReadSerializer(serializers.ModelSerializer):
	name = ComponentNameSerializer()
	approved_by = UserReadHandlersSerializer()
	user = UserReadHandlersSerializer()
	fault = FaultReadSerializer()
	class Meta:
		model = RequestPart
		fields = '__all__'

class RequestComponentUpdateSerializer(serializers.ModelSerializer):
	# name = ComponentNameSerializer()
	# user = UserReadHandlersSerializer()
	# fault = FaultReadSerializer()
	# approved_by = UserReadHandlersSerializer()
	approved_by = serializers.SlugRelatedField(
		queryset=User.objects.all(), slug_field='email'
	)
	class Meta:
		model = RequestComponent
		fields = '__all__'

class RequestPartUpdateSerializer(serializers.ModelSerializer):
	# name = ComponentNameSerializer()
	# user = UserReadHandlersSerializer()
	# fault = FaultReadSerializer()
	# approved_by = UserReadHandlersSerializer()
	approved_by = serializers.SlugRelatedField(
		queryset=User.objects.all(), slug_field='email'
	)
	class Meta:
		model = RequestPart
		fields = '__all__'