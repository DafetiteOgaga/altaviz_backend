from rest_framework import serializers
from .models import *

# Create your serializers here.
class ComponentNameSerializer(serializers.ModelSerializer):
	# components = ComponentSerializer(many=True, read_only=True)
	# parts = PartSerializer(many=True, read_only=True)
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
	# components = ComponentSerializer(many=True, read_only=True)
	# parts = PartSerializer(many=True, read_only=True)
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
