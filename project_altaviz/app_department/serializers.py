from rest_framework import serializers
from .models import *

# Create your serializers here.
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')