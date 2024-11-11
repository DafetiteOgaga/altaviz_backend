from rest_framework import serializers
from .models import *
# from app_users.serializers import UserSummarizedDetailsSerializer

# Create your serializers here.
class UserDeliveriesSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
		queryset = User.objects.all, slug_field='email'
	)
    class Meta:
        model = Deliveries
        fields = '__all__'

class ReadUserDeliveriresSerializer(serializers.ModelSerializer):
    # user = UserSummarizedDetailsSerializer(read_only=True)
    class Meta:
        model = Deliveries
        fields = ['id', 'deliveries']