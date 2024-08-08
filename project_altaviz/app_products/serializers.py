from rest_framework import serializers
from .models import *

# Create your serializers here.
class FeatureSerializer(serializers.ModelSerializer):
	class Meta:
		model = Feature
		fields = ['head', 'body']

class BenefitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Benefit
		fields = ['head', 'body']

class DescriptionSerializer(serializers.ModelSerializer):
	features = FeatureSerializer(many=True, read_only=True)
	benefits = BenefitSerializer(many=True, read_only=True)

	class Meta:
		model = Description
		fields = ['about', 'feature', 'benefit', 'conclusion', 'features', 'benefits']

class ProductSerializer(serializers.ModelSerializer):
	description = DescriptionSerializer(read_only=True)
	class Meta:
		model = Product
		fields = ['id', 'product_images', 'title', 'description']

	def get_product_images(self, obj):
		request = self.context.get('request')
		if obj.product_images:
			return request.build_absolute_uri(obj.product_images.url)
		return None
