from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from app_fault.views import engineerPendingFaults
from django.db.models import Q, Prefetch
# from app_sse_notification.views import send_sse_notification
from app_sse_notification.firebase_utils import send_notification

def compartmentalizedList(listValue: list):
	newDict = {}
	for item in listValue:
		_, id = item.split('-')
		if id not in newDict:
			newDict[id] = []
		newDict[id].append(item)
	return newDict
# Create your views here.
@api_view(['GET', 'POST'])
def componentName(request, pk=None):
	# get the records of the current components names from db
	component_details = ComponentName.objects.all()
	print(f'component_details: {component_details}')
	# make the queryset into a list
	listOfComponents = [comp.name for comp in component_details]
	exist = {}
	print(f'listOfComponents: {listOfComponents}')
	if request.method == 'POST':
		print('ITEM payload:', request.data)
		dicttn = {}
		# total length of request (without the user attribute)
		length = len(list(request.data)) - 1
		print(f'init len: {length}')
		for index, item in enumerate(list(request.data)):
			if item == 'user': continue
			item_value = request.data[item]
			# print(f'item:', item)

			# if the new name exists, dont create it
			if item_value in listOfComponents:
				exist[f'item-{index}'] = item_value
				print(f'item: {item_value} exists in {exist}')
				length -= 1
				return Response({'exist': f'{item_value} exists.'}, status=status.HTTP_200_OK)
			# cleanup the current data and add it to dicttn
			dicttn['name'] = item_value
			dicttn['user'] = request.data['user']
			print(f'dicttn:', dicttn)
			# serialize the dicttn
			serializer = ComponentNameSerializer(data=dicttn)
			print(f'is serializer valid:', serializer.is_valid())
			# print(f'serializer:', serializer)
			if serializer.is_valid():
				# update the database withh the new data
				serializer.save()
				print(f'current len: {length}')
				length -= 1
				print(f'new len: {length}')
				if length != 0:
					print(f'len is 0: {length == 0}')
					continue

				print('11111111111111')
				# update the component inventory table with the new data
				componentInventory = Component.objects.create(
					name=ComponentName.objects.get(name=dicttn['name']),
					user=User.objects.get(email=request.data['user'])
				)
				print('22222222222222')
				print(f'component inventory: {componentInventory.name}')
				print(f'component inventory qty: {componentInventory.quantity}')
				print(f'component inventory posted by: {componentInventory.user}')
				componentInventory.save()
				print('component inventory updated.')
				# send_notification(message='added component name to inventory')
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
			if not item.startswith('user'):
				print(f'new key item:', item[:-2])
				dicttn[item[:-2]] = dicttn.pop(item)
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
				# send_notification(message='updated component in inventory')
				return Response({'success': 'Success: Inventory has been updated.'}, status=status.HTTP_201_CREATED)
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
	# get the records of the current parts names from db
	parts_details = PartName.objects.all()
	print(f'parts_details: {parts_details}')
	# make the queryset into a list
	listOfParts = [part.name for part in parts_details]
	exist = {}
	print(f'listOfComponents: {listOfParts}')
	if request.method == 'POST':
		print('ITEM payload:', request.data)
		dicttn = {}
		# total length of request (without the user attribute)
		length = len(list(request.data)) - 1
		print(f'init len: {length}')
		for index, item in enumerate(list(request.data)):
			if item == 'user': continue
			item_value = request.data[item]
			# print(f'item:', item)

			# if the new name exists, dont create it
			if item_value in listOfParts:
				exist[f'item-{index}'] = item_value
				print(f'item: {item_value} exists in {exist}')
				length -= 1
				return Response({'exist': f'{item_value} exists.'}, status=status.HTTP_200_OK)
			# cleanup the current data and add it to dicttn
			dicttn['name'] = item_value
			dicttn['user'] = request.data['user']
			print(f'dicttn:', dicttn)
			# serialize the dicttn
			serializer = PartNameSerializer(data=dicttn)
			print(f'is serializer valid:', serializer.is_valid())
			# print(f'serializer:', serializer)
			if serializer.is_valid():
				# update the database withh the new data
				serializer.save()
				length -= 1
				if length != 0:
					continue
				# update the component inventory table with the new data
				partInventory = Part.objects.create(
					name=PartName.objects.get(name=dicttn['name']),
					user=User.objects.get(email=request.data['user'])
				)
				print('22222222222222')
				print(f'part inventory: {partInventory.name}')
				print(f'part inventory qty: {partInventory.quantity}')
				print(f'part inventory posted by: {partInventory.user}')
				partInventory.save()
				print('part inventory updated.')
				# send_notification(message='added part name to inventory')
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
			if not item.startswith('user'):
				print(f'new key item:', item[:-2])
				dicttn[item[:-2]] = dicttn.pop(item)
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
				# send_notification(message='updated part in inventory')
				return Response({'success': 'Success: Inventory has been updated.'}, status=status.HTTP_201_CREATED)
			print(f'serializer.errors: {serializer.errors}')
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	else:
		if pk:
			part_detail = Part.objects.get(pk=pk)
			print(f'part_detail: {part_detail} - with ID: {pk}')
			serializer = PartSerializer(part_detail)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			part_detail = Part.objects.all()
			print(f'part obj: {part_detail}')
			serializer = PartSerializer(part_detail, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'PATCH'])
def unapprovedPart(request, pk=None, type=None):
	print('################# end unapprovedPart #################')
	print(f'request type: {request.method}')
	print(f'pk: {pk}')
	if request.method == 'POST':
		print('PART payload:', request.data)
		partRequestList = [
			i for i in (list(request.data))
			if i.startswith('name') or
				i.startswith('quantity') or
				i.startswith('others') or
				i.startswith('reason')
		]
		dictOfLists = compartmentalizedList(partRequestList)
		length = len(list(dictOfLists))
		print(f'dictOfList: {dictOfLists}')
		print(f'dictOfList length: {length}')
		for key in dictOfLists.values():
			cleanedData = {
				'name': request.data[key[0]],
				'quantity': request.data[key[1]]
			}
			# print(f'cleanedData: {cleanedData}')
			cleanedData['user'] = request.data['user']
			# cleanedData['approved_by'] = None if request.data['approved_by'] == 'null' else request.data['approved_by']
			print(f'cleanedData: {cleanedData}')
			ptSerializer = UnconfirmedPartCreateSerializer(data=cleanedData)
			print(f'ptSerializer is valid: {ptSerializer.is_valid()}')
			if ptSerializer.is_valid():
				print(f'ptSerializer is valid')
				ptSerializer.save()
				print(f'ptSerializer saved #################')
			else:
				print(f'ptSerializer error: {ptSerializer.errors}')
				return Response({'error': 'Could not complete.'}, status=status.HTTP_201_CREATED)
		print('start send_notification ##########')
		send_notification(message='fixed part ready-hr')
		print('end send_notification ##########')
		print('################# end unapprovedPart #################')
		return Response({'received': 'Awaits approval.'}, status=status.HTTP_201_CREATED)
	elif request.method == 'PATCH':
		print('PART payload:', request.data)
		# return Response({'allgood'})
		# send either approved or rejected payload and handle the object accodingly

		# note: this setup is equally used in the patch method of requestComponent for
		# human-resource component request approval for workshop staffs
		# note: this code is missing incrementing the actual part component
		user = User.objects.get(pk=pk)
		print(f'user: {user}')
		print(f'user.role: {user.role}')
		part = UnconfirmedPart.objects.get(pk=request.data['faultID'])
		print(f'part: {part}')
		print(f'status (before)=> approved: {part.approved}, rejected: {part.rejected}')
		part.approved = request.data.get('approved')=='true'
		part.rejected = request.data.get('rejected')=='true'
		part.approved_by = user
		part.save()
		print(f'status (after)=> approved: {part.approved}, rejected: {part.rejected}')
		reaponse = 'approved' if part.approved else 'rejected'
		print('start send_notification ##########')
		send_notification(message='approve or reject fixed parts-hr')
		print('end send_notification ##########')
		return Response({'msg': reaponse}, status=status.HTTP_200_OK)
	elif request.method == 'GET':
		print('################# user unapprovedPart noti #################')
		if pk:
			user = User.objects.get(pk=pk)
			unapprovedPart = None
			if user.role == 'workshop':
				user = User.objects.prefetch_related(
					Prefetch(
						'partpostedby',  # The related name for the ForeignKey
						queryset=UnconfirmedPart.objects.filter(approved=False, rejected=False),  # Apply filtering
						to_attr='filtered_parts'  # Store the filtered related objects in this attribute
					)
				).get(pk=pk)
				print(f'user: {user}')
				# print(f'user: {user}')
				unapprovedPart = user.filtered_parts
			elif user.role == 'human-resource' or user.role == 'supervisor':
				unapprovedPart = UnconfirmedPart.objects.filter(approved=False, rejected=False)
			print(f'posted parts ids: {[part.id for part in unapprovedPart]}')
			partSerializer = UnconfirmedPartSerializer(instance=unapprovedPart, many=True).data
			for fixedPart in partSerializer:
				fixedPart['type'] = 'fixed-part'
			# partSerializer = [part['type'] = "part" for part in partSerializer]
			# for part in partSerializer:
			# 	part['type'] = 'part'
			print(f'role: {user.role}')
			if type == 'list':
				print(f'length of partSerializer: {len(partSerializer)}')
				return Response(partSerializer, status=status.HTTP_200_OK)
			elif type == 'notification':
				partSerializer = partSerializer[:5]
				print(f'length of partSerializer: {len(partSerializer)}')
				return Response(partSerializer, status=status.HTTP_200_OK)
			partRequestPaginator = PageNumberPagination()
			partRequestPaginator.page_size = 10  # Number of items per page
			paginatedRequest = partRequestPaginator.paginate_queryset(partSerializer, request)
			return partRequestPaginator.get_paginated_response(paginatedRequest)
		print('################# end user unapprovedPart noti #################')

@api_view(['DELETE'])
def deleteUnapprovedPart(request, pk=None):
	print(f'deleting ... ❌❌❌')
	try:
		item = UnconfirmedPart.objects.get(pk=pk)
		print(f'deleting ... : {item}')
		item.delete()
		print(f'done ✅✅✅')
		# send_notification(message='fixed part deleted')
		return Response({'msg': 'Posted Part deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
	except UnconfirmedPart.DoesNotExist:
		return Response({'msg': 'Part does not exist.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET',])
def approvedParts(request, pk=None):
	print('################# user approvedPart noti #################')
	if pk:
		user = User.objects.get(pk=pk)
		print(f'user: {user}')
		approvedPart = UnconfirmedPart.objects.filter(user=user, status=True)
		print(f'approvedPart: {approvedPart}')
		userApprovedPartsPaginator = PageNumberPagination()
		userApprovedPartsPaginator.page_size = 10  # Number of items per page
		paginatedRequest = userApprovedPartsPaginator.paginate_queryset(approvedPart, request)
		serializer = UnconfirmedPartSerializer(instance=paginatedRequest, many=True)
		# serializerData = serializer.data
		return userApprovedPartsPaginator.get_paginated_response(serializer.data)
	print('################# end user approvedPart noti #################')

@api_view(['GET',])
def totalUnapproved(request, pk=None):
	print('##################### total compRequests ###########################')
	user = User.objects.get(pk=pk)
	if user.role == 'human-resource':
		unapprovedUserPosts = UnconfirmedPart.objects.filter(approved=False, rejected=False)
	else:
		unapprovedUserPosts = UnconfirmedPart.objects.filter(user=user, approved=False, rejected=False)
	print(f'unapprovedUserPosts ids: {[post.id for post in unapprovedUserPosts]}')
	print('##################### end total compRequests ###########################')
	return Response({'total': len(unapprovedUserPosts)}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'PATCH'])
def requestComponent(request, pk=None, type=None):
	if request.method == 'POST':
		# note: only workshop would not require fault field
		print('################# requestComponent ####################')
		region = User.objects.get(email=request.data['user']).region
		print(f'region:', region.name)
		print(f'post payload: {request.data}')
		# dicttn = {}
		compRequestList = [
			i for i in (list(request.data))
			if i.startswith('name') or
				i.startswith('quantity') or
				i.startswith('others') or
				i.startswith('reason')
		]
		dictOfLists = compartmentalizedList(compRequestList)
		length = len(dictOfLists)
		_ = length
		print(f'dictOfList: {dictOfLists}')
		print(f'dictOfList length: {length}')
		responseInstances = []
		for key in dictOfLists.values():
			# print(f"""request.data.get("fault"): {request.data.get('fault')}""")
			cleanedData = {
				'name': request.data[key[0]],
				'quantityRequested': request.data[key[1]],
				'reason': request.data[key[2]],
				'fault': None if (request.data.get('fault') == 'null' or request.data.get('fault') == 'undefined') else request.data.get('fault'),
			}
			print(f'cleanedData: {cleanedData}')
			cleanedData['user'] = request.data['user']
			# cleanedData['fault'] = Fault.objects.get(id=request.data['fault'])
			print(f'cleanedData: {cleanedData}')
			requestSerializer = RequestComponentCreateSerializer(data=cleanedData)
			print(f'requestSerializer is valid: {requestSerializer.is_valid()}')
			if requestSerializer.is_valid():
				print(f'requestSerializer is valid')
				requestSerializer.save()
				print(f'requestSerializer saved #################')
				print(f'requestSerializer saved instance: {requestSerializer.instance}')
				responseInstances.append(RequestComponentReadSerializer(requestSerializer.instance).data)
			else:
				print(f'requestSerializer error: {requestSerializer.errors}')
		print('################# end requestComponent #################')
		response = 'Requests' if _ > 1 else f'{cleanedData["name"]} Request'
		print(f'length of requests: {_}')
		print(f'len responseInstances: {len(responseInstances)}')
		print(f'response: {response}')
		print('start send_notification ##########')
		send_notification(message=f'make component request-{region.name}')
		print('end send_notification ##########')
		return Response({'msg': f'{response} Received.', 'responseObjs': responseInstances}, status=status.HTTP_200_OK)
	elif request.method == 'PATCH':
		# note: only workshop would not require fault field
		print('################# requestComponent ####################')
		print(f'patch payload: {request.data}')
		componentRequest = RequestComponent.objects.get(pk=request.data['faultID'])
		print(f'componentRequest: {componentRequest}')
		region = componentRequest.user.region
		print(f'region: {region.name}')
		serializedComponentRequest = RequestComponentCreateSerializer(
			instance=componentRequest, data=request.data, partial=True
		)
		print(f'serializedComponentRequest is valid: {serializedComponentRequest.is_valid()}')
		# return Response({'msg':'allgood'})
		if serializedComponentRequest.is_valid():
			print(f'serializedComponentRequest is valid')
			serializedComponentRequest.save()
			print(f'serializedComponentRequest saved #################')
			updatedComponentRequest = RequestComponent.objects.get(pk=request.data['faultID'])
			print(f'status (after)=> approved: {updatedComponentRequest.approved}, rejected: {updatedComponentRequest.rejected}')
			reaponse = 'approved' if updatedComponentRequest.approved else 'rejected'
			print('start send_notification ##########')
			send_notification(message=f'approve/reject component request-{region.name}')
			print('end send_notification ##########')
			return Response({'msg': reaponse}, status=status.HTTP_200_OK)
			# return Response({'msg': 'Success'}, status=status.HTTP_200_OK)
		print(f'serializedComponentRequest.error: {serializedComponentRequest.errors}')
		return Response(serializedComponentRequest.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		if pk:
			# get this pagiated data using getpagination custom hook
			user = User.objects.get(pk=pk)
			print(f'user obj: {user}')
			if user.role == 'workshop':
				userRequest = RequestComponent.objects.filter(
				user=user, approved=False, rejected=False,
			)
			else:
				userRequest = RequestComponent.objects.filter(
				user=user, approved=False, rejected=False,
				fault__confirm_resolve=False
			)
			print(f'user request: {userRequest}')
			componentSerializer = RequestComponentReadSerializer(instance=userRequest, many=True).data
			for component in componentSerializer:
				component['type'] = 'component'
			# print(f'user: {user}')
			if type == 'list':
				print(f'length of componentSerializer: {len(componentSerializer)}')
				return Response(componentSerializer, status=status.HTTP_200_OK)
			elif type == 'notification':
				componentSerializer = componentSerializer[:5]
				print(f'length of componentSerializer: {len(componentSerializer)}')
				return Response(componentSerializer, status=status.HTTP_200_OK)
			componentRequestPaginator = PageNumberPagination()
			componentRequestPaginator.page_size = 10  # Number of items per page
			paginatedRequest = componentRequestPaginator.paginate_queryset(componentSerializer, request)
			return componentRequestPaginator.get_paginated_response(paginatedRequest)

@api_view(['GET',])
def totalPendingRequestComponent(request, pk=None):
	print('##################### total compRequests ###########################')
	user = User.objects.get(pk=pk)
	if user.role == 'workshop':
			compRequests = RequestComponent.objects.filter(
			user=user, approved=False, rejected=False,
		).count()
	else:
		compRequests = RequestComponent.objects.filter(
			user=user, approved=False, rejected=False,
			fault__confirm_resolve=False
		).count()
	print(f'compRequests: {compRequests}')
	print('##################### end total compRequests ###########################')
	return Response({'total': compRequests}, status=status.HTTP_200_OK)

@api_view(['DELETE',])
def deleteCompRequest(request, pk=None):
	print('##################### delete CompRequest ###########################')
	print(f'deleting ... ❌❌❌')
	try:
		compRequest = RequestComponent.objects.get(pk=pk)
	except:
		return Response({'error': 'compRequest not found'}, status=status.HTTP_404_NOT_FOUND)
	print(f'compRequest: {compRequest}')
	compRequest.delete()
	print(f'done ✅✅✅')
	print('start send_notification ##########')
	send_notification(message=f'component request deleted-{compRequest.fault.logged_by.branch.region.name if compRequest.fault else compRequest.user.region.name}')
	print('end send_notification ##########')
	print('##################### end delete CompRequest ###########################')
	return Response({'msg': 'deleted successfully'}, status=status.HTTP_200_OK)

@api_view(['GET',])
def approvedRequestComponent(request, pk=None):
	if pk:
		# get this pagiated data using getpagination custom hook
		user = User.objects.get(pk=pk)
		print(f'user obj: {user}')
		approvedUser = RequestComponent.objects.filter(user=user, approved=True)
		# print(f'approvedUser: {approvedUser}')
		approvedUserRequestPaginator = PageNumberPagination()
		approvedUserRequestPaginator.page_size = 10  # Number of items per page
		paginatedRequest = approvedUserRequestPaginator.paginate_queryset(approvedUser, request)
		usererializer = RequestComponentReadSerializer(instance=paginatedRequest, many=True)
		serialized_data = usererializer.data
		# print(f'usererializer: {usererializer.data}')
		return approvedUserRequestPaginator.get_paginated_response(serialized_data)

# ###################################
@api_view(['GET', 'POST', 'PATCH'])
def requestPart(request, pk=None, type=None):
	if request.method == 'POST':
		# note: only workshop would not require fault field
		print('################# requestPart ####################')
		region = User.objects.get(email=request.data['user']).region
		print(f'region:', region.name)
		print(f'post payload: {request.data}')
		# dicttn = {}
		partRequestList = [
			i for i in (list(request.data))
			if i.startswith('name') or
				i.startswith('quantity') or
				i.startswith('others') or
				i.startswith('reason')
		]
		dictOfLists = compartmentalizedList(partRequestList)
		length = len(dictOfLists)
		_ = length
		print(f'dictOfList: {dictOfLists}')
		print(f'dictOfList length: {length}')
		responseInstances = []
		for key in dictOfLists.values():
			cleanedData = {
				'name': request.data[key[0]],
				'quantityRequested': request.data[key[1]],
				'reason': request.data[key[2]],
				'fault': None if (request.data.get('fault') == 'null' or request.data.get('fault') == 'undefined') else request.data.get('fault'),
			}
			print(f'cleanedData: {cleanedData}')
			cleanedData['user'] = request.data['user']
			print(f'cleanedData: {cleanedData}')
			requestSerializer = RequestPartCreateSerializer(data=cleanedData)
			print(f'requestSerializer is valid: {requestSerializer.is_valid()}')
			if requestSerializer.is_valid():
				print(f'requestSerializer is valid')
				requestSerializer.save()
				print(f'requestSerializer saved #################')
				print(f'requestSerializer saved instance: {requestSerializer.instance}')
				responseInstances.append(RequestPartReadSerializer(requestSerializer.instance).data)
			else:
				print(f'requestSerializer error: {requestSerializer.errors}')
		print('################# end requestPart #################')
		response = 'Requests' if _ > 1 else f'{cleanedData["name"]} Request'
		print(f'length of requests: {_}')
		print(f'len responseInstances: {len(responseInstances)}')
		print(f'response: {response}')
		print('start send_notification ##########')
		send_notification(message=f'make part request-{region.name}')
		print('end send_notification ##########')
		return Response({'msg': f'{response} Received.', 'responseObjs': responseInstances}, status=status.HTTP_200_OK)
	elif request.method == 'PATCH':
		# note: only workshop would not require fault field
		print('################# requestPart ####################')
		print(f'patch payload: {request.data}')
		partRequest = RequestPart.objects.get(pk=request.data['faultID'])
		print(f'partRequest: {partRequest}')
		region = partRequest.user.region
		print(f'region: {region.name}')
		serializedPartRequest = RequestPartCreateSerializer(
			instance=partRequest, data=request.data, partial=True
		)
		print(f'serializedPartRequest is valid: {serializedPartRequest.is_valid()}')
		if serializedPartRequest.is_valid():
			print(f'serializedPartRequest is valid')
			serializedPartRequest.save()
			print(f'serializedPartRequest saved #################')
			print('start send_notification ##########')
			send_notification(message=f'approve/reject part request-{region.name}')
			print('end send_notification ##########')
			return Response({'msg': 'Success'}, status=status.HTTP_200_OK)
		print(f'serializedPartRequest.error: {serializedPartRequest.errors}')
		return Response(serializedPartRequest.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		if pk:
			# get this pagiated data using getpagination custom hook
			user = User.objects.get(pk=pk)
			print(f'user obj: {user}')

			if user.role == 'workshop':
				partRequest = RequestPart.objects.filter(
				user=user, approved=False, rejected=False,
			)
			else:
				partRequest = RequestPart.objects.filter(
				user=user, approved=False, rejected=False,
				fault__confirm_resolve=False
			)
			print(f'user request: {partRequest}')


			# partRequest = RequestPart.objects.filter(
			# 	user=user, approved=False, rejected=False,
			# 	fault__confirm_resolve=False
			# )
			partSerializer = RequestPartReadSerializer(instance=partRequest, many=True).data
			for part in partSerializer:
				part['type'] = 'part'
			# print(f'user: {user}')
			if type == 'list':
				print(f'length of partSerializer: {len(partSerializer)}')
				return Response(partSerializer, status=status.HTTP_200_OK)
			elif type == 'notification':
				partSerializer = partSerializer[:5]
				print(f'length of partSerializer: {len(partSerializer)}')
				return Response(partSerializer, status=status.HTTP_200_OK)
			partRequestPaginator = PageNumberPagination()
			partRequestPaginator.page_size = 10  # Number of items per page
			paginatedRequest = partRequestPaginator.paginate_queryset(partSerializer, request)
			return partRequestPaginator.get_paginated_response(paginatedRequest)

@api_view(['GET',])
def totalPendingRequestPart(request, pk=None):
	print('##################### total partRequests ###########################')
	user = User.objects.get(pk=pk)
	if user.role == 'workshop':
			partRequests = RequestPart.objects.filter(
			user=user, approved=False, rejected=False,
		).count()
	else:
		partRequests = RequestPart.objects.filter(
			user=user, approved=False, rejected=False,
			fault__confirm_resolve=False
		).count()
	# partRequests = RequestPart.objects.filter(
	# 	user=user,
	# 	approved=False,
	# 	rejected=False,
	# ).count()
	print(f'partRequests: {partRequests}')
	print('##################### end total partRequests ###########################')
	return Response({'total': partRequests}, status=status.HTTP_200_OK)

@api_view(['GET',])
def approvedRequestPart(request, pk=None):
	if pk:
		# get this pagiated data using getpagination custom hook
		user = User.objects.get(pk=pk)
		print(f'user obj: {user}')
		approvedUser = RequestPart.objects.filter(user=user, approved=True)
		# print(f'approvedUser: {approvedUser}')
		approvedUserRequestPaginator = PageNumberPagination()
		approvedUserRequestPaginator.page_size = 10  # Number of items per page
		paginatedRequest = approvedUserRequestPaginator.paginate_queryset(approvedUser, request)
		usererializer = RequestPartReadSerializer(instance=paginatedRequest, many=True)
		serialized_data = usererializer.data
		# print(f'usererializer: {usererializer.data}')
		return approvedUserRequestPaginator.get_paginated_response(serialized_data)

@api_view(['DELETE',])
def deletePartRequest(request, pk=None):
	print('##################### delete partRequest ###########################')
	print(f'deleting ... ❌❌❌')
	try:
		partRequest = RequestPart.objects.get(pk=pk)
	except:
		return Response({'error': 'partRequest not found'}, status=status.HTTP_404_NOT_FOUND)
	print(f'partRequest: {partRequest}')
	partRequest.delete()
	print(f'done ✅✅✅')
	print('start send_notification ##########')
	send_notification(message=f'part request deleted-{partRequest.fault.logged_by.branch.region.name if partRequest.fault else partRequest.user.region.name}')
	print('end send_notification ##########')
	print('##################### end delete partRequest ###########################')
	return Response({'msg': 'deleted successfully'}, status=status.HTTP_200_OK)

###################################################
@api_view(['GET'])
def regionUserRequests(request, pk=None, type=None):
	print('##################### regionUserRequests ###########################')
	# Get the help-desk user
	user = User.objects.get(pk=pk)
	# get the region of the help-desk
	region = user.region
	print(f'help-desk/supervisor: {user}')
	print(f'region: {region}')
	print()

	################ efficient code ########################
	# Fetch the unresolved faults queryset once
	unresolved_faults_queryset = Fault.objects.filter(
		verify_resolve=False,
		confirm_resolve=False,
	).prefetch_related('partfault', 'componentfault')

	# Now use this queryset in main query
	engineers = User.objects.filter(
		Q(role='engineer') | Q(role='supervisor'),
		# role='engineer',
		region=region,
		assignedto__in=unresolved_faults_queryset.filter(
			Q(partfault__isnull=False) | Q(componentfault__isnull=False)
		)
	).prefetch_related(
		Prefetch(
			'assignedto',
			queryset=unresolved_faults_queryset,
			to_attr='unresolved_faults'
		)
	).distinct()

	# allFaultsData = []  # Store all faults for all engineers
	allEngineersData = []  # Store all faults for all engineers
	# loop through retrieved engineers objects
	for eIndex, engineer in enumerate(engineers):
		# ascertain if current engineer has parts/components requests
		engineerSerializer = UserReadHandlersSerializer(instance=engineer).data
		partRequest = any([fault.partfault.exists() for fault in engineer.unresolved_faults])
		componentRequest = any([fault.componentfault.exists() for fault in engineer.unresolved_faults])
		print(f'comp: {componentRequest}, part: {partRequest}')
		print(f'{eIndex+1}. engineer: {engineer.first_name} - has requests: {partRequest or componentRequest}')

		print(f'component requests: {[f"faultID {fault.id}: {[comp.id for comp in fault.componentfault.all()]}" for fault in engineer.unresolved_faults if fault.componentfault.exists()]}')
		print(f'part requests: {[f"faultID {fault.id}: {[part.id for part in fault.partfault.all()]}" for fault in engineer.unresolved_faults if fault.partfault.exists()]}')
		faultInstances = [fault for fault in engineer.unresolved_faults if (fault.partfault.exists() or fault.componentfault.exists())]
		faultSerializer = FaultReadSerializer(
			instance=faultInstances,
			many=True
		).data
		print(f'	faults: {[fault["id"] for fault in faultSerializer]}')
		print(f'	faults: {[f"{fault.id} => confirm: {fault.confirm_resolve}" for fault in engineer.unresolved_faults]}')

		# Attach additional data to each fault
		for faultData, faultInstance in zip(faultSerializer, faultInstances):
			faultCompRequests = faultInstance.componentfault.all()
			faultPartRequests = faultInstance.partfault.all()
			# print(f'		fault: {faultInstance.id}')
			print(f'		compRequests: {[comp.id for comp in faultCompRequests]}, partrequest: {[part.id for  part in faultPartRequests]}')
			##############################################################
			##############################################################
			if not faultCompRequests and not faultPartRequests: continue
			##############################################################
			##############################################################
			print('\n')
			# print(f'	serializing fault: {faultInstance.id} #############')

			# Serialize component and part requests
			compRequestSerializer = RequestFaultComponentReadSerializer(faultCompRequests, many=True).data
			partRequestSerializer = RequestFaultPartReadSerializer(faultPartRequests, many=True).data

			# Add the serialized requests to the fault data
			faultData['requestComponent'] = compRequestSerializer if compRequestSerializer else False
			faultData['requestPart'] = partRequestSerializer if partRequestSerializer else False
			faultData['requestStatus'] = bool(compRequestSerializer) or bool(partRequestSerializer)
			# faultData['engineer'] = engineerSerializer
		engineerSerializer['faults'] = faultSerializer if faultSerializer else False

		# Add this fault to the overall list
		allEngineersData.append(engineerSerializer)
		# else:
		# 	print(f'Engineer {engineer} has no pending requests.')

	# If faults data is not empty, paginate the final list
	print('##################### end VVVVVVVVVVVVVVVVVV ###########################')
	if allEngineersData:
		if type == 'list':
			print(f'length of allEngineersData: {len(allEngineersData)}')
			return Response(allEngineersData, status=status.HTTP_200_OK)
		elif type == 'notification':
			allEngineersData = allEngineersData[:5]
			print(f'length of allEngineersData: {len(allEngineersData)}')
			return Response(allEngineersData, status=status.HTTP_200_OK)
		userPaginator = PageNumberPagination()
		userPaginator.page_size = 10  # Number of items per page
		paginated_allFaultsData = userPaginator.paginate_queryset(allEngineersData, request)
		print('##################### end engineerUnconfirmedFaults ###########################')
		return userPaginator.get_paginated_response(paginated_allFaultsData)
	return Response({'message': 'No faults found for any engineers'}, status=status.HTTP_200_OK)

@api_view(['GET',])
def totalRegionUserRequests(request, pk=None):
	print('##################### total totalRegionUserRequests ###########################')
	helpdesk = User.objects.get(pk=pk)
	print(f'help-desk (totalRegionUserRequests): {helpdesk}')
	region = helpdesk.region
	print(f'region: {region}')
	# Fetch the unresolved faults queryset once
	unresolved_faults_queryset = Fault.objects.filter(
		verify_resolve=False,
		confirm_resolve=False,
	).prefetch_related('partfault', 'componentfault')

	# Now use this queryset in main query
	engineers = User.objects.filter(
		Q(role='engineer') | Q(role='supervisor'),
		# role='engineer',
		region=region,
		assignedto__in=unresolved_faults_queryset.filter(
			Q(partfault__isnull=False) | Q(componentfault__isnull=False)
		)
	).prefetch_related(
		Prefetch(
			'assignedto',
			queryset=unresolved_faults_queryset,
			to_attr='unresolved_faults'
		)
	).distinct()

	print(f'engineers: {engineers}')
	print(f'engineers: {engineers}')
	print(f'total count: {len(engineers)}')
	print('##################### end total totalRegionUserRequests ###########################')
	return Response({'total': len(engineers)}, status=status.HTTP_200_OK)

###################################################
@api_view(['GET'])
def unconfirmedRegionResolutions(request, pk=None, type=None):
	print('##################### unconfirmedRegionResolutions ###########################')
	user = User.objects.get(pk=pk)
	region = user.region
	print(f'help-desk user: {user}')
	print(f'region: {region}')

	# Fetch all engineers from the same region
	engineers = User.objects.filter(
		Q(role='engineer') | Q(role='supervisor'),
		region=region
	).prefetch_related(
		Prefetch(
			'assignedto',
			queryset=Fault.objects.filter(
				confirm_resolve=False
			).prefetch_related(
				'partfault',
				'componentfault'
			),
			to_attr='unresolved_faults'
		)
	).distinct()
	print(f'Engineers length: {len(engineers)}')
	engineers = list(filter(lambda engineer: engineer.unresolved_faults != [], engineers))
	print(f'Engineers length: {len(engineers)}')
	# print(f'Engineers: {engineers}')
	# [[print(f'id: {fault.id}: {fault.confirm_resolve}') for fault in engineer.unresolved_faults] for engineer in engineers]
	print()

	allEngineersData = []  # Store all faults for all engineers
	count = 0

	# Iterate over each engineer
	for eIndex, engineer in enumerate(engineers):
		print(f'Checking engineer: {engineer}')

		engineerSerializer = UserReadHandlersSerializer(instance=engineer).data
		partRequest = any([fault.partfault.exists() for fault in engineer.unresolved_faults])
		componentRequest = any([fault.componentfault.exists() for fault in engineer.unresolved_faults])
		print(f'{eIndex+1}. engineer: {engineer.first_name} - has requests: {partRequest or componentRequest}')
		faultInstances = engineer.unresolved_faults
		print(f'	component requests: {[f"faultID {fault.id}: {[comp.id for comp in fault.componentfault.all()]}" for fault in engineer.unresolved_faults if fault.componentfault.exists()]}')
		print(f'	part requests: {[f"faultID {fault.id}: {[part.id for part in fault.partfault.all()]}" for fault in engineer.unresolved_faults if fault.partfault.exists()]}')
		count += len(faultInstances)
		faultSerializer = FaultReadSerializer(faultInstances, many=True).data
		print(f'		faults: {[fault.id for fault in faultInstances]}')
		# print(f'			faults: {[f"{fault.id}, verified: {fault.verify_resolve}, confirm: {fault.confirm_resolve}" for fault in faultInstances]}')
		# print(f'			faults: {[f"{fault.id}, confirm: {fault.confirm_resolve}" for fault in faultInstances]}')
		# serializedFaults = faultSerializer.data
		print()
		for faultData, faultInstance in zip(faultSerializer, faultInstances):
			# if faultInstance.componentfault.exists() or faultInstance.partfault.exists():
			faultCompRequests = faultInstance.componentfault.all()
			faultPartRequests = faultInstance.partfault.all()

			# Serialize component and part requests
			compRequestSerializer = RequestFaultComponentReadSerializer(faultCompRequests, many=True)
			partRequestSerializer = RequestFaultPartReadSerializer(faultPartRequests, many=True)

			# Add the serialized requests to the fault data
			faultData['requestComponent'] = compRequestSerializer.data if compRequestSerializer.data else False
			faultData['requestPart'] = partRequestSerializer.data if partRequestSerializer.data else False
			faultData['requestStatus'] = bool(compRequestSerializer.data) or bool(partRequestSerializer.data)

		engineerSerializer['faults'] = faultSerializer if faultSerializer else False

		# Add this fault to the overall list
		allEngineersData.append(engineerSerializer)
	print(f'total faults: {count}')
	print('##################### end UUUUUUUUUUUUUUUU ###########################')
	if allEngineersData:
		if type == 'list':
			print(f'length of allEngineersData: {len(allEngineersData)}')
			return Response(allEngineersData, status=status.HTTP_200_OK)
		elif type == 'notification':
			allEngineersData = allEngineersData[:5]
			print(f'length of allEngineersData: {len(allEngineersData)}')
			return Response(allEngineersData, status=status.HTTP_200_OK)
		userPaginator = PageNumberPagination()
		userPaginator.page_size = 10  # Number of items per page
		paginated_allFaultsData = userPaginator.paginate_queryset(allEngineersData, request)
		return userPaginator.get_paginated_response(paginated_allFaultsData)
	return Response({'message': 'No faults found for any engineers'}, status=status.HTTP_200_OK)

@api_view(['GET',])
def totalUnconfirmedRegionResolutions(request, pk=None):
	print('##################### total totalUnconfirmedRegionResolutions ###########################')
	helpdesk = User.objects.get(pk=pk)
	print(f'help-desk (totalUnconfirmedRegionResolutions): {helpdesk}')
	region = helpdesk.region
	print(f'region: {region}')
	engineers = User.objects.filter(
		Q(role='engineer') | Q(role='supervisor'),
		# role='engineer',
		region=region
	).prefetch_related(
		# Prefetch faults with confirm_resolve=False
		Prefetch(
			'assignedto',
			queryset=Fault.objects.filter(
				# verify_resolve=True,
				confirm_resolve=False
			).prefetch_related(
				# Prefetch related part and component requests (if they exist)
				'partfault',
				'componentfault'
			),
			to_attr='unresolved_faults'
		)
	).distinct()
	print(f'Engineers length: {len(engineers)}')
	engineers = list(filter(lambda engineer: engineer.unresolved_faults != [], engineers))
	print(f'engineers: {engineers}')
	print(f'total count: {len(engineers)}')
	print('##################### end total totalUnconfirmedRegionResolutions ###########################')
	return Response({'total': len(engineers)}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
def requestStatus(request, pk=None):
	if request.method == 'PATCH':
		print(f'PATCH payload: {request.data}')
		print(f'list version of payload: {list(request.data)}')
		requestList = list(request.data)
		print(f'request list: {requestList}')
		cleanedData = {}
		cleanedData['approved_by'] = request.data['approved_by']
		if 'approved' in requestList: cleanedData['approved'] = request.data['approved']
		if 'rejected' in requestList: cleanedData['rejected'] = request.data['rejected']
		print(f'cleanedData: {cleanedData}')
		if 'requestComponentIds' in requestList: print(f'requestcomp Payload: {request.data["requestComponentIds"]}')
		if 'requestPartIDs' in requestList: print(f'requestpart Payload: {request.data["requestPartIDs"]}')
		region = None
		if 'requestComponentIds' in requestList:
			for compRequestID in request.data['requestComponentIds'].split(','):
				print(f'compRequestID: {compRequestID}')
				# print(f'type of value: {type(compRequestID)}')
				# compRequestID = int(compRequestID)
				# print(f'type of value: {type(compRequestID)}')
				compRequestInstance = RequestComponent.objects.get(pk=compRequestID)
				region = compRequestInstance.fault.logged_by.branch.region.name
				# print(f'approved: {compRequestInstance.approved}, rejected: {compRequestInstance.rejected}')
				if compRequestInstance.approved or compRequestInstance.rejected:
					print(f'Request component {compRequestID} has already been responded to. Skipping...')
					continue
				# print(f'status: {compRequestInstance.approved or compRequestInstance.rejected}')
				compSerializer = RequestComponentUpdateSerializer(instance=compRequestInstance, data=cleanedData, partial=True)
				print(f'compSerializer is valid: {compSerializer.is_valid()}')
				if compSerializer.is_valid():
					compSerializer.save()
					print(f'compSerializer for request {compRequestID} is saved successfully. ##################')
				print(f'compserializer error: {compSerializer.errors}')
				# print()
		# return Response({'allgood'})
		if 'requestPartIDs' in requestList:
			for partRequestID in request.data['requestPartIDs'].split(','):
				partRequestInstance = RequestPart.objects.get(pk=partRequestID)
				region = compRequestInstance.fault.logged_by.branch.region
				if partRequestInstance.approved or partRequestInstance.rejected:
					print(f'Request part {partRequestID} has already been responded to. Skipping...')
					continue
				partSerializer = RequestPartUpdateSerializer(instance=partRequestInstance, data=cleanedData, partial=True)
				print(f'partSerializer is valid: {partSerializer.is_valid()}')
				if partSerializer.is_valid():
					partSerializer.save()
					print(f'partSerializer for request {partRequestID} is saved successfully. ##################')
				print(f'partSerializer error: {partSerializer.errors}')
		print('start send_notification ##########')
		send_notification(message=f'approve/reject components and/or parts request-{region.name}')
		print('end send_notification ##########')
		return Response({'msg': 'success'}, status=status.HTTP_200_OK)
	return Response({'wrong method used'}, status=status.HTTP_200_OK)

###################################################
@api_view(['GET'])
def faultsWithRequests(request, pk=None):
	print('##################### faultsWithRequests ###########################')
	# fetch users who are engineers, have unconfirmed faults and have part/component (or both) requests
	engineers = User.objects.filter(
		role='engineer'  # Fetch users who are engineers
	).filter(
		Q(assignedto__isnull=False) &  # Ensure the engineer has assigned faults
		(
			Q(assignedto__partfault__isnull=False) |  # Faults with part requests
			Q(assignedto__componentfault__isnull=False)  # Faults with component requests
		) & (
			# Part fault conditions
			(
				Q(assignedto__partfault__approved=False) &
				Q(assignedto__partfault__rejected=False)
			) |
			# Component fault conditions
			(
				Q(assignedto__componentfault__approved=False) &
				Q(assignedto__componentfault__rejected=False)
			)
		)
	).prefetch_related(
		'assignedto__partfault',  # Fetch related part requests
		'assignedto__componentfault'  # Fetch related component requests
	).distinct()  # Prevent duplicates

	allFaultsData = []  # Store all faults for all engineers

	countVerified = 0
	countUnverified = 0
	totalVerified = 0
	# countUnresolved = 0
	# loop through retrieved engineers objects
	for eIndex, engineer in enumerate(engineers):
		# ascertain if current engineer has parts/components requests
		partRequest = any([fault.partfault.exists() for fault in engineer.assignedto.all()])
		componentRequest = any([fault.componentfault.exists() for fault in engineer.assignedto.all()])
		print(f'{eIndex+1}. engineer: {engineer.first_name} - has requests: {partRequest or componentRequest}')
		# print(f'part: {partRequest}')
		# print(f'comp: {componentRequest}')

		# checks if engineer has faults and requests
		if partRequest or componentRequest:
			# print(f'{eIndex+1}. {engineer.email} has request')
			# get the fault instances
			faultInstances = engineer.assignedto.filter(confirm_resolve=False, verify_resolve=False)
			print(f'len fault instances: {len(faultInstances)}')
			# print(f'fault instances: {eIndex+1}')
			# Serialize faults data
			faultSerializer = FaultReadSerializer(
				instance=faultInstances,
				many=True
			).data
			print(f'serialized faults IDs: {[fault["id"] for fault in faultSerializer]}')

			# Serialize the engineer data
			engineerSerializer = UserReadHandlersSerializer(instance=engineer).data

			# Attach additional data to each fault
			# note: engineer.assignedto.all() holds all the parts and components requests
			for faultData, faultsRequests in zip(faultSerializer, faultInstances):
				# print(f'faultData: {faultData["id"]}: len faultSerializer: {len(faultSerializer)} - len faultInstances: {len(faultInstances)}')
				faultCompRequests = faultsRequests.componentfault.filter(approved=False, rejected=False) # component requests for current fault
				faultPartRequests = faultsRequests.partfault.filter(approved=False, rejected=False) # part requests for current fault

				if faultData["verify_resolve"] == True: countVerified += 1
				if faultData["verify_resolve"] == False: countUnverified += 1
				# if faultData["verify_resolve"] == False and faultData["verify_resolve"] == False: countUnresolved += 1
				totalVerified += 1

				print(f'	fault id: {faultData["id"]} - verify:{faultData["verify_resolve"]} - resolved:{faultData["confirm_resolve"]}')
				print(f'		comp ids (not verified nor rejected): {[comp.id for comp in faultCompRequests]}')
				print(f'		part ids (not verified nor rejected): {[part.id for part in faultPartRequests]}')

				# Serialize component and part requests
				compRequestSerializer = RequestFaultComponentReadSerializer(faultCompRequests, many=True).data
				partRequestSerializer = RequestFaultPartReadSerializer(faultPartRequests, many=True).data

				# exclude faults without requests
				if not (bool(compRequestSerializer) or bool(partRequestSerializer)): continue
				print(f'	########## fault with request (passed) ##########: {faultsRequests.id}')

				# Add the serialized requests to the fault data
				faultData['requestComponent'] = compRequestSerializer if compRequestSerializer else False
				faultData['requestPart'] = partRequestSerializer if partRequestSerializer else False
				faultData['requestStatus'] = bool(compRequestSerializer) or bool(partRequestSerializer)
				faultData['engineer'] = engineerSerializer

				# Add this fault to the overall list
				allFaultsData.append(faultData)

	# print(f'fault instances: {len(faultInstances)}')
	print()
	print(f'verified: {countVerified}')
	print(f'unverified: {countUnverified}')
	# print(f'countUnresolved: {countUnresolved}')
	print(f'total: {totalVerified}')

	# If faults data is not empty, paginate the final list
	if allFaultsData:
		print(f'len of all faults data: {len(allFaultsData)}')
		paginator = PageNumberPagination()
		paginator.page_size = 10  # Items per page
		paginated_faults = paginator.paginate_queryset(allFaultsData, request)
		return paginator.get_paginated_response(paginated_faults)

	return Response({'message': 'No faults found for any engineers'}, status=status.HTTP_200_OK)

@api_view(['GET',])
def totalFaultsWithRequests(request, pk=None):
	print('##################### total totalFaultsWithRequests ###########################')
	engineers = User.objects.filter(
		role='engineer'  # Fetch users who are engineers
	).filter(
		Q(assignedto__isnull=False) &  # Ensure the engineer has assigned faults
		(
			Q(assignedto__partfault__isnull=False) |  # Faults with part requests
			Q(assignedto__componentfault__isnull=False)  # Faults with component requests
		) & (
			# Part fault conditions
			(
				Q(assignedto__partfault__approved=False) &
				Q(assignedto__partfault__rejected=False)
			) |
			# Component fault conditions
			(
				Q(assignedto__componentfault__approved=False) &
				Q(assignedto__componentfault__rejected=False)
			)
		)
	).prefetch_related(
		'assignedto__partfault',  # Fetch related part requests
		'assignedto__componentfault'  # Fetch related component requests
	).distinct()  # Prevent duplicates

	# skip engineers with confirmed faults and unapproved and unrejected requests
	count = 0
	filteredEngineers = []
	for eIndex, engineer in enumerate(engineers):
		print(f'{eIndex+1}. engineer: {engineer}')
		for fIndex, fault in enumerate(engineer.assignedto.filter(confirm_resolve=False, verify_resolve=False)):
			print(f'	{fIndex+1}. fault: {fault.id} verify:{fault.verify_resolve} resolved:{fault.confirm_resolve}')
			partRequests = [request.id for request in fault.partfault.filter(approved=False, rejected=False)]
			componentRequests = [request.id for request in fault.componentfault.filter(approved=False, rejected=False)]
			print(f'		part: {[request.id for request in fault.partfault.filter(approved=False, rejected=False)]}')
			print(f'		comp: {[request.id for request in fault.componentfault.filter(approved=False, rejected=False)]}')
			if not (bool(partRequests) or bool(componentRequests)): continue
			print(f'engineer {engineer.first_name} with fault {fault.id} passed ###########')
			filteredEngineers.append(engineer)
			count += 1

	# find the length of affected engineers
	print(f'total engineers: {[engineer.id for engineer in filteredEngineers]}')
	print('##################### end total totalFaultsWithRequests ###########################')
	return Response({'total': count}, status=status.HTTP_200_OK)

@api_view(['GET'])
def unapprovedWorkshopRequests(request, pk=None, type=None):
	print('################# user unapprovedWorkshopRequests #################')
	print(f'request type: {request.method}')
	print(f'pk: {pk}')
	# if request.method == 'GET':
	user = User.objects.prefetch_related(
		Prefetch(
			'partpostedby',  # The related name for the ForeignKey
			queryset=UnconfirmedPart.objects.filter(approved=False, rejected=False),  # Apply filtering
			to_attr='filtered_parts'  # Store the filtered related objects in this attribute
		),
		Prefetch(
			'componentrequestuser',  # The related name for the ForeignKey
			queryset=RequestComponent.objects.filter(approved=False, rejected=False),  # Apply filtering
			to_attr='filtered_components'  # Store the filtered related objects in this attribute
		)
	).get(pk=pk)
	print(f'user: {user}')
	# print(f'user: {user}')
	unapprovedPart = user.filtered_parts
	unapprovedComponent = user.filtered_components
	combinedLists = user.filtered_components + user.filtered_parts
	print(f'combined ids: {[comb.id for comb in combinedLists]}')
	print(f'posted parts ids: {[part.id for part in unapprovedPart]}')
	print(f'component ids: {[component.id for component in unapprovedComponent]}')

	componentSerializer = RequestComponentReadSerializer(instance=unapprovedComponent, many=True).data
	for comp in componentSerializer:
		comp['type'] = 'component'
	partSerializer = UnconfirmedPartSerializer(instance=unapprovedPart, many=True).data
	for part in partSerializer:
		part['type'] = 'part'
	combinedSerializedItems = componentSerializer + partSerializer
	print(f'role: {user.role}')
	if type == 'list':
		print(f'length of combinedSerializedItems: {len(combinedSerializedItems)}')
		return Response(combinedSerializedItems, status=status.HTTP_200_OK)
	elif type == 'notification':
		combinedSerializedItems = combinedSerializedItems[:5]
		print(f'length of combinedSerializedItems: {len(combinedSerializedItems)}')
		return Response(combinedSerializedItems, status=status.HTTP_200_OK)
	partRequestPaginator = PageNumberPagination()
	partRequestPaginator.page_size = 10  # Number of items per page
	paginatedRequest = partRequestPaginator.paginate_queryset(combinedSerializedItems, request)
	print('################# end user unapprovedWorkshopRequests noti #################')
	return partRequestPaginator.get_paginated_response(paginatedRequest)

####################################################################
########### hr #####################
@api_view(['GET'])
def allUserRequests(request, pk=None, type=None):
	print('##################### regionUserRequests ###########################')
	# Get the help-desk user
	user = User.objects.get(pk=pk)
	# get the region of the help-desk
	role = user.role
	print(f'human-resource: {user}')
	print(f'role: {role}')
	print()

	################ efficient code ########################
	# Fetch the unresolved faults queryset once
	unresolved_faults_queryset = Fault.objects.filter(
		Q(partfault__isnull=False) | Q(componentfault__isnull=False),
		Q(partfault__approved=False, partfault__rejected=False) |
		Q(componentfault__approved=False, componentfault__rejected=False),
		verify_resolve=False,
		confirm_resolve=False,
	).distinct().prefetch_related('partfault', 'componentfault')

	print(f'unresolved_faults_queryset: {unresolved_faults_queryset}')
	# Now use this queryset in main query
	engineers = User.objects.filter(
		Q(role='engineer') | Q(role='supervisor'),
		# role='engineer',
		## region=region,
		assignedto__in=unresolved_faults_queryset.filter(
			Q(partfault__isnull=False) | Q(componentfault__isnull=False)
		)
	).prefetch_related(
		Prefetch(
			'assignedto',
			queryset=unresolved_faults_queryset,
			to_attr='unresolved_faults'
		)
	).distinct()

	print(f'engineers: {engineers}')

	# allFaultsData = []  # Store all faults for all engineers
	allEngineersData = []  # Store all faults for all engineers

	# loop through retrieved engineers objects
	for eIndex, engineer in enumerate(engineers):
		# ascertain if current engineer has parts/components requests
		engineerSerializer = UserReadHandlersSerializer(instance=engineer).data
		partRequest = any([fault.partfault.exists() for fault in engineer.unresolved_faults])
		componentRequest = any([fault.componentfault.exists() for fault in engineer.unresolved_faults])
		print(f'comp: {componentRequest}, part: {partRequest}')
		print(f'{eIndex+1}. engineer: {engineer.first_name} - has requests: {partRequest or componentRequest}')

		print(f'component requests: {[f"faultID {fault.id}: {[comp.id for comp in fault.componentfault.all()]}" for fault in engineer.unresolved_faults if fault.componentfault.exists()]}')
		print(f'part requests: {[f"faultID {fault.id}: {[part.id for part in fault.partfault.all()]}" for fault in engineer.unresolved_faults if fault.partfault.exists()]}')

		faultInstances = [fault for fault in engineer.unresolved_faults if (fault.partfault.exists() or fault.componentfault.exists())]
		# faultInstances = engineer.assignedto.filter(confirm_resolve=False, verify_resolve=False)
		
		# print()
		# Serialize faults data
		faultSerializer = FaultReadSerializer(
			instance=faultInstances,
			many=True
		).data

		print(f'	faults: {[fault["id"] for fault in faultSerializer]}')
		print(f'	faults: {[f"{fault.id} => confirm: {fault.confirm_resolve}" for fault in engineer.unresolved_faults]}')

		# print()
		# Attach additional data to each fault
		for faultData, faultInstance in zip(faultSerializer, faultInstances):
			faultCompRequests = faultInstance.componentfault.all()
			faultPartRequests = faultInstance.partfault.all()
			# print(f'		fault: {faultInstance.id}')
			print(f'		compRequests: {[comp.id for comp in faultCompRequests]}, partrequest: {[part.id for  part in faultPartRequests]}')
			##############################################################
			##############################################################
			if not faultCompRequests and not faultPartRequests: continue
			##############################################################
			##############################################################
			print('\n')
			# print(f'	serializing fault: {faultInstance.id} #############')

			# Serialize component and part requests
			compRequestSerializer = RequestFaultComponentReadSerializer(faultCompRequests, many=True).data
			for component in compRequestSerializer:
				component['type'] = 'component'
			partRequestSerializer = RequestFaultPartReadSerializer(faultPartRequests, many=True).data
			for part in partRequestSerializer:
				part['type'] = 'part'

			# Add the serialized requests to the fault data
			faultData['requestComponent'] = compRequestSerializer if compRequestSerializer else False
			faultData['requestPart'] = partRequestSerializer if partRequestSerializer else False
			faultData['requestStatus'] = bool(compRequestSerializer) or bool(partRequestSerializer)
			# faultData['engineer'] = engineerSerializer
		engineerSerializer['faults'] = faultSerializer if faultSerializer else False

		# Add this fault to the overall list
		allEngineersData.append(engineerSerializer)
		# else:
		# 	print(f'Engineer {engineer} has no pending requests.')

	# If faults data is not empty, paginate the final list
	print('##################### end VVVVVVVVVVVVVVVVVV ###########################')
	if allEngineersData:
		if type == 'list':
			print(f'length of allEngineersData: {len(allEngineersData)}')
			return Response(allEngineersData, status=status.HTTP_200_OK)
		elif type == 'notification':
			allEngineersData = allEngineersData[:5]
			print(f'length of allEngineersData: {len(allEngineersData)}')
			return Response(allEngineersData, status=status.HTTP_200_OK)
		userPaginator = PageNumberPagination()
		userPaginator.page_size = 10  # Number of items per page
		paginated_allFaultsData = userPaginator.paginate_queryset(allEngineersData, request)
		print('##################### end engineerUnconfirmedFaults ###########################')
		return userPaginator.get_paginated_response(paginated_allFaultsData)
	return Response({'message': 'No faults found for any engineers'}, status=status.HTTP_200_OK)

@api_view(['GET',])
def totalAllUserRequests(request, pk=None):
	print('##################### total totalRegionUserRequests ###########################')
	helpdesk = User.objects.get(pk=pk)
	print(f'help-desk (totalRegionUserRequests): {helpdesk}')
	region = helpdesk.region
	print(f'region: {region}')
	# Fetch the unresolved faults queryset once
	unresolved_faults_queryset = Fault.objects.filter(
		Q(partfault__isnull=False) | Q(componentfault__isnull=False),
		Q(partfault__approved=False, partfault__rejected=False) |
		Q(componentfault__approved=False, componentfault__rejected=False),
		verify_resolve=False,
		confirm_resolve=False,
	).distinct().prefetch_related('partfault', 'componentfault')

	# Now use this queryset in main query
	engineers = User.objects.filter(
		Q(role='engineer') | Q(role='supervisor'),
		# role='engineer',
		## region=region,
		assignedto__in=unresolved_faults_queryset.filter(
			Q(partfault__isnull=False) | Q(componentfault__isnull=False)
		)
	).prefetch_related(
		Prefetch(
			'assignedto',
			queryset=unresolved_faults_queryset,
			to_attr='unresolved_faults'
		)
	).distinct()

	print(f'engineers: {engineers}')
	print(f'engineers: {engineers}')
	print(f'total count: {len(engineers)}')
	print('##################### end total totalRegionUserRequests ###########################')
	return Response({'total': len(engineers)}, status=status.HTTP_200_OK)

@api_view(['GET'])
def workshopRequests(request, pk=None, type=None):
	print('##################### workshopRequests ###########################')
	user = User.objects.get(pk=pk)
	print(f'user: {user}')
	componentRequests = RequestComponent.objects.filter(
		user__role='workshop',
		approved=False,
		rejected=False
	)
	[print(f'componentID: {component.id}, approved: {component.approved}, rejected: {component.rejected}, dept: {component.user.role}, user: {component.user.first_name}') for component in componentRequests]
	# return Response({'allgood'})
	serializedComponents = RequestComponentReadSerializer(instance=componentRequests, many=True).data
	for component in serializedComponents:
		component['type'] = 'component'
	if type == 'list':
		print(f'length of serializedComponents: {len(serializedComponents)}')
		return Response(serializedComponents, status=status.HTTP_200_OK)
	elif type == 'notification':
		serializedComponents = serializedComponents[:5]
		print(f'length of serializedComponents: {len(serializedComponents)}')
		return Response(serializedComponents, status=status.HTTP_200_OK)
	userPaginator = PageNumberPagination()
	userPaginator.page_size = 10  # Number of items per page
	paginated_components = userPaginator.paginate_queryset(serializedComponents, request)
	# print('##################### end engineerUnconfirmedFaults ###########################')
	return userPaginator.get_paginated_response(paginated_components)

@api_view(['GET'])
def totalWorkshopRequests(request, pk=None, type=None):
	print('##################### totalWorkshopRequests ###########################')
	user = User.objects.get(pk=pk)
	print(f'user: {user}')
	componentRequests = RequestComponent.objects.filter(
		user__role='workshop',
		approved=False,
		rejected=False
	)
	total = len(componentRequests)
	print(f'total: {total}')
	# print(f'total count: {len(engineers)}')
	print('##################### end totalWorkshopRequests ###########################')
	return Response({'total': total}, status=status.HTTP_200_OK)

@api_view(['GET'])
def allRequestsOnly(request, pk=None, type=None):
	print('################# allRequestsOnly #################')
	print(f'request type: {request.method}')
	print(f'pk: {pk}')
	user = User.objects.get(pk=pk)
	partRequests = RequestPart.objects.filter(
		Q(fault__isnull=True) | (
        Q(fault__confirm_resolve=False) &
        Q(fault__verify_resolve=False)
		),
		approved=False,
		rejected=False
	)
	componentRequests = RequestComponent.objects.filter(
		Q(fault__isnull=True) | (
        Q(fault__confirm_resolve=False) &
        Q(fault__verify_resolve=False)
		),
		approved=False,
		rejected=False
	)
	fixedParts = UnconfirmedPart.objects.filter(
		approved=False,
		rejected=False
	)
	print(f'user: {user}')
	print()
	print(f'components >>>>>>>>>>')
	for comp in componentRequests:
		print(f'componentID: {comp.id}')
		print(f'approved: {comp.approved}')
		print(f'rejected: {comp.rejected}')
		if comp.fault:
			print(f'fault verify_resolve: {comp.fault.verify_resolve}')
			print(f'fault confirm_resolve: {comp.fault.confirm_resolve}')
		else: print('no fault ######')
		print(f'user: {comp.user.first_name}')
		print()
	print()
	print(f'parts >>>>>>>>>>')
	for part in partRequests:
		print(f'partID: {part.id}')
		print(f'approved: {part.approved}')
		print(f'rejected: {part.rejected}')
		if part.fault:
			print(f'fault verify_resolve: {part.fault.verify_resolve}')
			print(f'fault confirm_resolve: {part.fault.confirm_resolve}')
		else: print('no fault ######')
		print(f'user: {part.user.first_name}')
		print()

	componentSerializer = RequestComponentReadSerializer(instance=componentRequests, many=True).data
	for comp in componentSerializer:
		comp['type'] = 'component'
	partSerializer = RequestPartReadSerializer(instance=partRequests, many=True).data
	for part in partSerializer:
		part['type'] = 'part'
	fixedPartsSerializer = UnconfirmedPartSerializer(instance=fixedParts, many=True).data
	for fixedPart in fixedPartsSerializer:
		fixedPart['type'] = 'fixed-part'
	combinedSerializedItems = componentSerializer + partSerializer + fixedPartsSerializer
	# print(f'role: {user.role}')
	if type == 'list':
		print(f'length of combinedSerializedItems: {len(combinedSerializedItems)}')
		return Response(combinedSerializedItems, status=status.HTTP_200_OK)
	elif type == 'notification':
		combinedSerializedItems = combinedSerializedItems[:5]
		print(f'length of combinedSerializedItems: {len(combinedSerializedItems)}')
		return Response(combinedSerializedItems, status=status.HTTP_200_OK)
	partRequestPaginator = PageNumberPagination()
	partRequestPaginator.page_size = 10  # Number of items per page
	paginatedRequest = partRequestPaginator.paginate_queryset(combinedSerializedItems, request)
	print('################# end user unapprovedWorkshopRequests noti #################')
	return partRequestPaginator.get_paginated_response(paginatedRequest)
