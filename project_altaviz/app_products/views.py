from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

# Create your views here.
@api_view(['GET', 'POST'])
def product(request, pk=None):
	if request.method == 'POST':
		print('payload:', request.data)
		serializer = ProductSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			product_details = Product.objects.all()
			print('###################### product (post) ##########################')
			# for i, obj in enumerate(product_details):
			# 	print(f'{i+1}. {obj.title}')
			print('###################### end product (post) ##########################')
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		print(f'serializer.errors: {serializer.errors}')
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	else:
		if pk:
			product_details = get_object_or_404(Product.objects.select_related('description').prefetch_related('description__features', 'description__benefits'), pk=pk)
			# desc = product_details.description.get(pk=pk)
			print('###################### product pk (get) ##########################')
			# [print(f'{i+1}. {obj.title}') for i, obj in enumerate(product_details)]
			print('######################')
			# [print(f'{i+1}. {obj.about[:10]}') for i, obj in enumerate(desc)]
			print('###################### end product pk (get) ##########################')
			serializer = ProductSerializer(product_details, context={'request': request})
		else:
			product_details = Product.objects.select_related('description').prefetch_related('description__features', 'description__benefits').all()
			print(f'Product obj: {product_details}')
			print('###################### product (get) ##########################')
			# for i, obj in enumerate(product_details):
			# 	print(f'{i+1}. {obj.title}')
			print('###################### end product (get) ##########################')
			serializer = ProductSerializer(product_details, many=True, context={'request': request})
	
	return Response(serializer.data)


# @api_view(['GET', 'POST'])
# def product(request, pk):
# 	if request.method == 'POST':
# 		print('payload:', request.data)
# 		# return Response({
# 		#     'message': 'success. payload recieved',
# 		#     'yes': 'done.'
# 		#     })
# 		serializer = ProductSerializer(data=request.data)
# 		print(f'serializer: {serializer}')
# 		print(f'serializer.is_valid: {serializer.is_valid()}')
# 		print(f'serializer.errors: {serializer.errors}')
# 		if serializer.is_valid():
# 			serializer.save()
			
# 			product_details = Product.objects.all()
# 			print('###################### product (post) ##########################')
# 			# [print(f'{i+1}. {obj.title} by: {obj.description[:10]}') for i, obj, in enumerate(contacts)]
# 			print('###################### end product (post) ##########################')
			
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 	product_details = Product.objects.all()
# 	print(f'Product obj: {product_details}')
# 	print('###################### product (get) ##########################')
# 	# [print(f'{i+1}. {obj.title} by: {obj.description[:10]}') for i, obj, in enumerate(contacts)]
# 	print('###################### end product (get) ##########################')
	
# 	serializer = ProductSerializer(product_details, many=True)
# 	return Response(serializer.data)
# 	# return Response({"home": "welcome home from django server. This information is from the backend server"}, status=status.HTTP_200_OK)
