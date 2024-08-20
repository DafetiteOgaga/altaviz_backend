from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

# Create your views here.
@api_view(['GET', 'POST'])
def componentName(request, pk=None):
	component_details = ComponentName.objects.all()
	print(f'component_details: {component_details}')
	listOfComponents = [comp.name for comp in component_details]
	exist = {}
	print(f'listOfComponents: {listOfComponents}')
	if request.method == 'POST':
		print('ITEM payload:', request.data)
		dicttn = {}
		length = len(list(request.data))
		for index, item in enumerate(list(request.data)):
			item_value = request.data[item]
			# print(f'item:', item)
			if item_value in listOfComponents:
				exist[f'item-{index}'] = item_value
				print(f'item: {item_value} exists in {exist}')
				length -= 1
				return Response({'exist': f'{item_value} exists.'}, status=status.HTTP_200_OK)
			dicttn['name'] = item_value
			print(f'dicttn:', dicttn)
			serializer = ComponentNameSerializer(data=dicttn)
			print(f'is serializer valid:', serializer.is_valid())
			# print(f'serializer:', serializer)
			if serializer.is_valid():
				serializer.save()
				length -= 1
				if length != 0:
					continue
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			print(f'serializer.errors: {serializer.errors}')
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	else:
		if pk:
			component_detail = get_object_or_404(ComponentName, pk=pk)
			print(f'component_detail: {component_detail} - with ID: {pk}')
			serializer = ComponentNameSerializer(component_detail)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			# component_details = ComponentName.objects.all()
			print(f'component obj: {component_details}')
			serializer = ComponentNameSerializer(component_details, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def components(request, pk=None):
	if request.method == 'POST':
		print('COMPONENT payload:', request.data)
		dicttn = {}
		length = len(list(request.data))
		print('list version:', list(request.data))
		print('length:', length)
		for item in list(request.data):
			print(f'item:', item)
			dicttn[item] = request.data[item]
			print(f'prev dicttn:', dicttn)
			# item = item[:-3]
			print(f'new key item:', item[:-3])
			dicttn[item[:-3]] = dicttn.pop(item)
			print(f'new dicttn:', dicttn)
			serializer = ComponentSerializer(data=dicttn)
			print(f'is serializer valid:', serializer.is_valid())
			if serializer.is_valid():
				length -= 1
				if length % 2	== 0:
					serializer.save()
					print(f'saved: {dicttn}')
				if length != 0:
					continue
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			print(f'serializer.errors: {serializer.errors}')
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	else:
		if pk:
			component_detail = get_object_or_404(Component, pk=pk)
			print(f'component_detail: {component_detail} - with ID: {pk}')
			serializer = ComponentSerializer(component_detail)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			component_details = Component.objects.all()
			print(f'Component obj: {component_details}')
			serializer = ComponentSerializer(component_details, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def partName(request, pk=None):
	parts_details = PartName.objects.all()
	print(f'parts_details: {parts_details}')
	listOfParts = [part.name for part in parts_details]
	exist = {}
	print(f'listOfComponents: {listOfParts}')
	if request.method == 'POST':
		print('ITEM payload:', request.data)
		dicttn = {}
		length = len(list(request.data))
		for index, item in enumerate(list(request.data)):
			item_value = request.data[item]
			# print(f'item:', item)
			if item_value in listOfParts:
				exist[f'item-{index}'] = item_value
				print(f'item: {item_value} exists in {exist}')
				length -= 1
				return Response({'exist': f'{item_value} exists.'}, status=status.HTTP_200_OK)
			dicttn['name'] = item_value
			print(f'dicttn:', dicttn)
			serializer = PartNameSerializer(data=dicttn)
			print(f'is serializer valid:', serializer.is_valid())
			# print(f'serializer:', serializer)
			if serializer.is_valid():
				serializer.save()
				length -= 1
				if length != 0:
					continue
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			print(f'serializer.errors: {serializer.errors}')
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	else:
		if pk:
			part_details = get_object_or_404(PartName, pk=pk)
			print(f'part_details: {part_details} - with ID: {pk}')
			serializer = PartNameSerializer(part_details)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			part_details = PartName.objects.all()
			print(f'part obj: {part_details}')
			serializer = PartNameSerializer(part_details, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def parts(request, pk=None):
	if request.method == 'POST':
		print('PART payload:', request.data)
		dicttn = {}
		length = len(list(request.data))
		print('list version:', list(request.data))
		print('length:', length)
		for item in list(request.data):
			print(f'item:', item)
			dicttn[item] = request.data[item]
			print(f'prev dicttn:', dicttn)
			# item = item[:-3]
			print(f'new key item:', item[:-3])
			dicttn[item[:-3]] = dicttn.pop(item)
			print(f'new dicttn:', dicttn)
			serializer = PartSerializer(data=dicttn)
			print(f'is serializer valid:', serializer.is_valid())
			if serializer.is_valid():
				length -= 1
				if length % 2	== 0:
					serializer.save()
					print(f'saved: {dicttn}')
				if length != 0:
					continue
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			print(f'serializer.errors: {serializer.errors}')
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	else:
		if pk:
			part_detail = get_object_or_404(Part, pk=pk)
			print(f'part_detail: {part_detail} - with ID: {pk}')
			serializer = PartSerializer(part_detail)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			part_detail = Part.objects.all()
			print(f'part obj: {part_detail}')
			serializer = PartSerializer(part_detail, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
