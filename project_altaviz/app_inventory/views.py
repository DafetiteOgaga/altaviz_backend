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
from asgiref.sync import async_to_sync, sync_to_async

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
	if request.method == 'POST':
		print('ITEM payload:', request.data)
		async def postData():
			component_details = await sync_to_async(lambda: list(ComponentName.objects.all()))()
			# print(f'component_details: {component_details}')
			# make the queryset into a list
			listOfComponents = [comp.name for comp in component_details]
			exist = {}
			print(f'listOfComponents: {listOfComponents}')
			dicttn = {}
			# total length of request (without the user attribute)
			length = len(list(request.data))-1
			print(f'init len: {length}')
			for index, item in enumerate(list(request.data)):
				if item == 'user': continue
				item_value = request.data[item]
				# print(f'item:', item)

				# if the new name exists, dont create it
				if item_value in listOfComponents:
					exist[f'item-{index}'] = item_value
					print(f'item: {item_value} exists in the inventory list')
					length -= 1
					return Response({'exist': f'{item_value} exists.'}, status=status.HTTP_200_OK)
				# cleanup the current data and add it to dicttn
				dicttn['name'] = item_value
				dicttn['user'] = request.data['user']
				print(f'dicttn:', dicttn)
				# serialize the dicttn
				serializer = await sync_to_async(lambda: ComponentNameSerializer(data=dicttn))()
				print(f'is serializer valid:', await sync_to_async(serializer.is_valid)())
				# print(f'serializer:', serializer)
				if await sync_to_async(serializer.is_valid)():
					# update the database withh the new data
					await sync_to_async(serializer.save)()
					print(f'current len: {length}')
					length -= 1
					print(f'new len: {length}')
					if length != 0:
						print(f'len is 0: {length == 0}')
						continue

					print('11111111111111')
					# update the component inventory table with the new data
					name = await sync_to_async(ComponentName.objects.get)(name=dicttn['name'])
					user = await sync_to_async(User.objects.get)(email=request.data['user'])
					componentInventory = await sync_to_async(lambda: Component.objects.create(
						name=name,
						user=user
					))()
					print('22222222222222')
					print(f'component inventory: {componentInventory.name}')
					print(f'component inventory qty: {componentInventory.quantity}')
					print(f'component inventory posted by: {componentInventory.user}')
					await sync_to_async(componentInventory.save)()
					print('component inventory updated.')
					# send_notification(message='added component name to inventory')
					return Response(serializer.data, status=status.HTTP_201_CREATED)
				print(f'serializer.errors: {serializer.errors}')
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		return async_to_sync(postData)()
	else:
		if pk:
			async def getAComponentName():
				component_detail = await sync_to_async(ComponentName.objects.get)(pk=pk)
				print(f'component_detail: {component_detail} - with ID: {pk}')
				serializer = await sync_to_async(lambda: ComponentNameSerializer(component_detail).data)()
				return Response(serializer, status=status.HTTP_200_OK)
			return async_to_sync(getAComponentName)()
		else:
			async def getAllComponentNames():
				component_details = await sync_to_async(lambda: list(ComponentName.objects.all()))()
				print(f'component_details: {component_details}')
				serializer = await sync_to_async(lambda: ComponentNameSerializer(component_details, many=True).data)()
				return Response(serializer, status=status.HTTP_200_OK)
			return async_to_sync(getAllComponentNames)()

@api_view(['GET', 'POST'])
def components(request, pk=None):
	if request.method == 'POST':
		async def postComponent():
			print('in async fxn')
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
				serializer = await sync_to_async(lambda: ComponentSerializer(data=dicttn))()
				print(f'is serializer valid:', await sync_to_async(serializer.is_valid)())
				if await sync_to_async(serializer.is_valid)():
					length -= 1
					if length % 2	== 0:
						await sync_to_async(serializer.save)()
						print(f'saved: {dicttn}')
					if length != 0:
						continue
					# send_notification(message='updated component in inventory')
					return Response({'success': 'Success: Inventory has been updated.'}, status=status.HTTP_201_CREATED)
				print(f'serializer.errors: {serializer.errors}')
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		return async_to_sync(postComponent)()
	else:
		if pk:
			async def getAComponent():
				component_detail = await sync_to_async(Component.objects.select_related('user', 'name').get)(pk=pk)
				print(f'component_detail: {component_detail.name.name} - with ID: {pk}')
				serializer = await sync_to_async(lambda: ComponentSerializer(component_detail).data)()
				return Response(serializer, status=status.HTTP_200_OK)
			return async_to_sync(getAComponent)()
		else:
			async def getAllComponents():
				component_details = await sync_to_async(lambda: list(Component.objects.all()))()
				# print(f'Component obj: {component_details}')
				serializer = await sync_to_async(lambda: ComponentSerializer(component_details, many=True).data)()
				return Response(serializer, status=status.HTTP_200_OK)
			return async_to_sync(getAllComponents)()


@api_view(['GET', 'POST'])
def partName(request, pk=None):
	# get the records of the current parts names from db
	if request.method == 'POST':
		print('ITEM payload:', request.data)
		async def postPart():
			parts_details = await sync_to_async(lambda: list(PartName.objects.all()))()
			print(f'parts_details: {parts_details}')
			# make the queryset into a list
			listOfParts = [part.name for part in parts_details]
			exist = {}
			print(f'listOfComponents: {listOfParts}')
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
					print(f'item: {item_value} exists in inentory')
					length -= 1
					return Response({'exist': f'{item_value} exists.'}, status=status.HTTP_200_OK)
				# cleanup the current data and add it to dicttn
				dicttn['name'] = item_value
				dicttn['user'] = request.data['user']
				print(f'dicttn:', dicttn)
				# serialize the dicttn
				serializer = await sync_to_async(lambda: PartNameSerializer(data=dicttn))()
				print(f'is serializer valid:', await sync_to_async(serializer.is_valid)())
				# print(f'serializer:', serializer)
				if await sync_to_async(serializer.is_valid)():
					# update the database withh the new data
					await sync_to_async(serializer.save)()
					length -= 1
					if length != 0:
						continue
					# update the component inventory table with the new data
					name = await sync_to_async(PartName.objects.get)(name=dicttn['name'])
					user = await sync_to_async(User.objects.get)(email=request.data['user'])
					partInventory = await sync_to_async(lambda: Part.objects.create(
						name=name,
						user=user
					))()
					print('22222222222222')
					print(f'part inventory: {partInventory.name}')
					print(f'part inventory qty: {partInventory.quantity}')
					print(f'part inventory posted by: {partInventory.user}')
					await sync_to_async(partInventory.save)()
					print('part inventory updated.')
					# send_notification(message='added part name to inventory')
					return Response(serializer.data, status=status.HTTP_201_CREATED)
				print(f'serializer.errors: {serializer.errors}')
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		return async_to_sync(postPart)()
	else:
		if pk:
			async def getPartName():
				part_details = await sync_to_async(PartName.objects.get)(pk=pk)
				print(f'part_details: {part_details} - with ID: {pk}')
				serializer = await sync_to_async(lambda: PartNameSerializer(part_details).data)()
				return Response(serializer, status=status.HTTP_200_OK)
			return async_to_sync(getPartName)()
		else:
			async def getAllPartNames():
				part_details = await sync_to_async(lambda: list(PartName.objects.all()))()
				print(f'part obj: {part_details}')
				serializer = await sync_to_async(lambda: PartNameSerializer(part_details, many=True).data)()
				return Response(serializer, status=status.HTTP_200_OK)
			return async_to_sync(getAllPartNames)()

@api_view(['GET', 'POST'])
def parts(request, pk=None):
	if request.method == 'POST':
		async def postPart():
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
				serializer = await sync_to_async(lambda: PartSerializer(data=dicttn))()
				print(f'is serializer valid:', await sync_to_async(serializer.is_valid)())
				if await sync_to_async(serializer.is_valid)():
					length -= 1
					if length % 2	== 0:
						await sync_to_async(serializer.save)()
						print(f'saved: {dicttn}')
					if length != 0:
						continue
					# send_notification(message='updated part in inventory')
					return Response({'success': 'Success: Inventory has been updated.'}, status=status.HTTP_201_CREATED)
				print(f'serializer.errors: {serializer.errors}')
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		return async_to_sync(postPart)()
	else:
		if pk:
			async def getPart():
				part_detail = await sync_to_async(Part.objects.get)(pk=pk)
				# print(f'part_detail: {part_detail} - with ID: {pk}')
				serializer = await sync_to_async(lambda: PartSerializer(part_detail).data)()
				return Response(serializer, status=status.HTTP_200_OK)
			return async_to_sync(getPart)()
		else:
			async def getAllParts():
				part_detail = await sync_to_async(lambda: list(Part.objects.all()))()
				# print(f'part obj: {part_detail}')
				serializer = await sync_to_async(lambda: PartSerializer(part_detail, many=True).data)()
				return Response(serializer, status=status.HTTP_200_OK)
			return async_to_sync(getAllParts)()

@api_view(['GET', 'POST', 'PATCH'])
def unapprovedPart(request, pk=None, type=None):
	print('################# end unapprovedPart #################')
	print(f'request type: {request.method}')
	print(f'pk: {pk}')
	if request.method == 'POST':
		async def postData():
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
				nameOfPart = await sync_to_async(PartName.objects.get)(name=request.data[key[0]])
				cleanedData = {
					'name': nameOfPart.id,
					'quantity': request.data[key[1]]
				}
				# print(f'cleanedData: {cleanedData}')
				cleanedData['user'] = request.data['user']
				# cleanedData['approved_by'] = None if request.data['approved_by'] == 'null' else request.data['approved_by']
				print(f'cleanedData: {cleanedData}')
				ptSerializer = await sync_to_async(lambda: UnconfirmedPartCreateSerializer(data=cleanedData))()
				print(f'ptSerializer is valid: {await sync_to_async(ptSerializer.is_valid)()}')
				if await sync_to_async(ptSerializer.is_valid)():
					print(f'ptSerializer is valid')
					await sync_to_async(ptSerializer.save)()
					print(f'ptSerializer saved #################')
				else:
					print(f'ptSerializer error: {ptSerializer.errors}')
					return Response({'error': 'Could not complete.'}, status=status.HTTP_201_CREATED)
			print('start send_notification ##########')
			await sync_to_async(send_notification)(message='fixed part ready-hr')
			print('end send_notification ##########')
			print('################# end unapprovedPart #################')
			return Response({'received': 'Awaits approval.'}, status=status.HTTP_201_CREATED)
		return async_to_sync(postData)()
	elif request.method == 'PATCH':
		# ###############################################################
		# ###############################################################
		# ###############################################################
		# ###############################################################
		# note: augment the fixed part into part model to increase part count
		# ###############################################################
		# ###############################################################
		# ###############################################################
		# ###############################################################
		async def patchData():
			print('in async fxn')
			print('PART payload:', request.data)
			# return Response({'allgood'})
			# send either approved or rejected payload and handle the object accodingly

			# note: this setup is equally used in the patch method of requestComponent for
			# human-resource component request approval for workshop staffs
			# note: this code is missing incrementing the actual part component
			user = await sync_to_async(User.objects.get)(pk=pk)
			print(f'user: {user}')
			print(f'user.role: {user.role}')
			idKey = request.data.get('requestID') or request.data.get('itemID')
			part = await sync_to_async(UnconfirmedPart.objects.select_related('name').get)(pk=idKey)
			print(f'part: {part}')
			print(f'status (before)=> approved: {part.approved}, rejected: {part.rejected}')
			part.approved = request.data.get('approved')=='true'
			part.rejected = request.data.get('rejected')=='true'
			part.approved_by = user
			await sync_to_async(part.save)()
			print(f'status (after)=> approved: {part.approved}, rejected: {part.rejected}')
			print(f'fixed part name: {part.name.name}')
			print(f'fixed part quantity: {part.quantity}')
			if request.data.get('approved') == 'true':
				partialData = {'name': part.name.name, 'quantity': part.quantity, 'action': False}
				inventoryUpdateserializer = await sync_to_async(lambda: PartSerializer(data=partialData))()
				print(f'is serializer valid:', await sync_to_async(inventoryUpdateserializer.is_valid)())
				if await sync_to_async(inventoryUpdateserializer.is_valid)():
					await sync_to_async(inventoryUpdateserializer.save)()
					print(f'saved: {inventoryUpdateserializer.data}')
				else:
					print(f'serializer.errors: {inventoryUpdateserializer.errors}')
					return Response(inventoryUpdateserializer.errors, status=status.HTTP_400_BAD_REQUEST)
			reaponse = 'approved' if part.approved else 'rejected'
			print('start send_notification ##########')
			await sync_to_async(send_notification)(message='approve or reject fixed parts-hr')
			print('end send_notification ##########')
			return Response({'msg': reaponse}, status=status.HTTP_200_OK)
		return async_to_sync(patchData)()
	elif request.method == 'GET':
		print('################# user unapprovedPart noti #################')
		if pk:
			async def getItem():
				user = await sync_to_async(User.objects.get)(pk=pk)
				print(f'user: {user.first_name} - {user.role}')
				unapprovedPart = None
				if user.role == 'workshop':
					prefetchedData = Prefetch(
						'partpostedby',  # The related name for the ForeignKey
						queryset=UnconfirmedPart.objects.filter(approved=False, rejected=False, user=user),  # Apply filtering
						to_attr='filtered_parts'  # Store the filtered related objects in this attribute
					)
					user = await sync_to_async(lambda: User.objects.prefetch_related(prefetchedData).get(pk=pk))()
					print(f'user: {user}')
					unapprovedPart = user.filtered_parts
					print(f'unapprovedPart:', unapprovedPart)
				elif user.role == 'human-resource' or user.role == 'supervisor':
					unapprovedPart = await sync_to_async(lambda: list(UnconfirmedPart.objects.filter(approved=False, rejected=False)))()
				print(f'posted parts ids: {[part.id for part in unapprovedPart]}')
				partSerializer = await sync_to_async(lambda: UnconfirmedPartSerializer(instance=unapprovedPart, many=True).data)()
				for fixedPart in partSerializer:
					fixedPart['type'] = 'fixed-part'
				# partSerializer = [part['type'] = "part" for part in partSerializer]
				# for part in partSerializer:
				# 	part['type'] = 'part'
				print(f'role: {user.role}')
				return partSerializer
			partSerializer = async_to_sync(getItem)()
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
	async def deleteUPart():
		print(f'deleting ... ❌❌❌')
		try:
			item = await sync_to_async(UnconfirmedPart.objects.get)(pk=pk)
			print(f'deleting ... : {item}')
			await sync_to_async(item.delete)()
			print(f'done ✅✅✅')
			# send_notification(message='fixed part deleted')
			return Response({'msg': 'Posted Part deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
		except UnconfirmedPart.DoesNotExist:
			return Response({'msg': 'Part does not exist.'}, status=status.HTTP_404_NOT_FOUND)
	return async_to_sync(deleteUPart)()

@api_view(['GET',])
def approvedParts(request, pk=None):
	# i think i intend to use this for user notification. alerting them if
	# their request was approved/rejected. however, i am yet to implement this
	print('################# user approvedPart noti #################')
	if pk:
		async def getApprovedPart():
			user = await sync_to_async(User.objects.get)(pk=pk)
			print(f'user: {user}')
			approvedPart = await sync_to_async(lambda: list(UnconfirmedPart.objects.filter(Q(approved=True)|Q(rejected=True), user=user,)))()
			print(f'approvedPart: {approvedPart}')
			userApprovedPartsPaginator = PageNumberPagination()
			userApprovedPartsPaginator.page_size = 10  # Number of items per page
			paginatedRequest = userApprovedPartsPaginator.paginate_queryset(approvedPart, request)
			serializer = UnconfirmedPartSerializer(instance=paginatedRequest, many=True)
			# serializerData = serializer.data
			return userApprovedPartsPaginator.get_paginated_response(serializer.data)
		return async_to_sync(getApprovedPart)()
	print('################# end user approvedPart noti #################')

@api_view(['GET',])
def totalUnapproved(request, pk=None):
	async def getTotalUnapproved():
		print('##################### total compRequests ###########################')
		user = await sync_to_async(User.objects.get)(pk=pk)
		if user.role == 'human-resource':
			unapprovedUserPosts = await sync_to_async(lambda: list(UnconfirmedPart.objects.filter(approved=False, rejected=False)))()
		else:
			unapprovedUserPosts = await sync_to_async(lambda: list(UnconfirmedPart.objects.filter(user=user, approved=False, rejected=False)))()
		print(f'unapprovedUserPosts ids: {[post.id for post in unapprovedUserPosts]}')
		print('##################### end total compRequests ###########################')
		return Response({'total': len(unapprovedUserPosts)}, status=status.HTTP_200_OK)
	return async_to_sync(getTotalUnapproved)()

@api_view(['GET', 'POST', 'PATCH'])
def requestComponent(request, pk=None, type=None):
	if request.method == 'POST':
		print(f'post payload: {request.data}')
		async def postComponentRequest():
			# note: only workshop would not require fault field
			print('################# requestComponent ####################')
			user = await sync_to_async(User.objects.select_related('region').get)(email=request.data['user'])
			region = user.region.name
			print(f'region:', region)
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
				requestSerializer = await sync_to_async(lambda: RequestComponentCreateSerializer(data=cleanedData))()
				print(f'requestSerializer is valid: {await sync_to_async(requestSerializer.is_valid)()}')
				if await sync_to_async(requestSerializer.is_valid)():
					print(f'requestSerializer is valid')
					await sync_to_async(requestSerializer.save)()
					print(f'requestSerializer saved #################')
					print(f'requestSerializer saved instance: {requestSerializer.instance}')
					responseInstances.append(await sync_to_async(lambda: RequestComponentReadSerializer(requestSerializer.instance).data)())
				else:
					print(f'requestSerializer error: {requestSerializer.errors}')
			print('################# end requestComponent #################')
			response = 'Requests' if _ > 1 else f'{cleanedData["name"]} Request'
			print(f'length of requests: {_}')
			print(f'len responseInstances: {len(responseInstances)}')
			print(f'response: {response}')
			print('start send_notification ##########')
			await sync_to_async(send_notification)(message=f'make component request-{region}')
			print('end send_notification ##########')
			return Response({'msg': f'{response} Received.', 'responseObjs': responseInstances}, status=status.HTTP_200_OK)
		return async_to_sync(postComponentRequest)()
	elif request.method == 'PATCH':
		async def patchData():
			print(f'patch payload: {request.data}')
			# note: only workshop would not require fault field
			print('################# requestComponent ####################')
			componentRequest = await sync_to_async(RequestComponent.objects.select_related(
				'user__region', 'name'
			).get)(pk=request.data['requestID'])
			print(f'componentRequest: {componentRequest}')
			region = componentRequest.user.region.name
			print(f'region: {region}')
			serializedComponentRequest = await sync_to_async(lambda: RequestComponentCreateSerializer(
				instance=componentRequest, data=request.data, partial=True
			))()
			print(f'serializedComponentRequest is valid: {await sync_to_async(serializedComponentRequest.is_valid)()}')
			# return Response({'msg':'allgood'})
			if await sync_to_async(serializedComponentRequest.is_valid)():
				if request.data.get('approved'):
					partialData = {
						'name': componentRequest.name.name,
						'quantity': componentRequest.quantityRequested,
						'user': request.data['approved_by'],
					}
					UpdateComponentSerializer = await sync_to_async(
					lambda: ComponentSerializer(
							data=partialData, context={'action': True}
						)
					)()
					print(f'is serializer valid:', await sync_to_async(UpdateComponentSerializer.is_valid)())
					if await sync_to_async(UpdateComponentSerializer.is_valid)():
						print(f'removing {componentRequest.quantityRequested} items from {componentRequest.name.name} in inventory')
						await sync_to_async(UpdateComponentSerializer.save)()
				await sync_to_async(serializedComponentRequest.save)()
				print(f'serializedComponentRequest saved #################')
				updatedComponentRequest = await sync_to_async(RequestComponent.objects.get)(pk=request.data['requestID'])
				print(f'status (after)=> approved: {updatedComponentRequest.approved}, rejected: {updatedComponentRequest.rejected}')
				reaponse = 'approved' if updatedComponentRequest.approved else 'rejected'
				print('start send_notification ##########')
				await sync_to_async(send_notification)(message=f'approve/reject component request-{region}')
				print('end send_notification ##########')
				return Response({'msg': reaponse}, status=status.HTTP_200_OK)
				# return Response({'msg': 'Success'}, status=status.HTTP_200_OK)
			print(f'serializedComponentRequest.error: {serializedComponentRequest.errors}')
			return Response(serializedComponentRequest.errors, status=status.HTTP_400_BAD_REQUEST)
		return async_to_sync(patchData)()
	elif request.method == 'GET':
		if pk:
			async def getComponentRequest():
				print('in getComponentRequest fxn')
				# get this pagiated data using getpagination custom hook
				user = await sync_to_async(User.objects.get)(pk=pk)
				print(f'user obj: {user}')
				if user.role == 'workshop':
					userRequest = await sync_to_async(lambda: list(RequestComponent.objects.filter(
					user=user, approved=False, rejected=False,
				)))()
				else:
					userRequest = await sync_to_async(lambda: list(RequestComponent.objects.filter(
					user=user, approved=False, rejected=False,
					fault__confirm_resolve=False, fault__verify_resolve=False
				)))()
				print(f'user request: {userRequest}')
				componentSerializer = await sync_to_async(lambda: RequestComponentReadSerializer(instance=userRequest, many=True).data)()
				for component in componentSerializer:
					component['type'] = 'component'
				return componentSerializer
			componentSerializer = async_to_sync(getComponentRequest)()
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
	async def getTotalPendingRequestComponent():
		print('##################### total compRequests ###########################')
		user = await sync_to_async(User.objects.get)(pk=pk)
		if user.role == 'workshop':
				compRequests = await sync_to_async(lambda: list(RequestComponent.objects.filter(
				user=user, approved=False, rejected=False,
			)))()
		else:
			compRequests = await sync_to_async(lambda: list(RequestComponent.objects.filter(
				user=user, approved=False, rejected=False,
				fault__confirm_resolve=False, fault__verify_resolve=False
			)))()
		print(f'compRequests: {len(compRequests)}')
		print('##################### end total compRequests ###########################')
		return Response({'total': len(compRequests)}, status=status.HTTP_200_OK)
	return async_to_sync(getTotalPendingRequestComponent)()

@api_view(['DELETE',]) # stopped here and untested
def deleteCompRequest(request, pk=None):
	# consider sending the pk of the user making the request to use in filtering the
	# select related db hit
	async def deleteComponentRequest():
		print('##################### delete CompRequest ###########################')
		print(f'deleting ... ❌❌❌❌❌❌')
		branchRegion = None
		try:
			compRequest = await sync_to_async(RequestComponent.objects.select_related(
				'user__region', 'fault__logged_by__branch__region'
			).get)(pk=pk)
			branchRegion = compRequest.fault.logged_by.branch.region.name
			print(f'branchRegion: {branchRegion}')
		except AttributeError:
			compRequest = await sync_to_async(RequestComponent.objects.select_related(
				'user__region'
			).get)(pk=pk)
		except:
			return Response({'error': 'compRequest not found'}, status=status.HTTP_404_NOT_FOUND)
		print(f'compRequest: {compRequest}')
		userRegion = compRequest.user.region.name
		print(f'userRegion: {userRegion}')
		await sync_to_async(compRequest.delete)()
		print(f'done ✅✅✅')
		print('start send_notification ##########')
		await sync_to_async(send_notification)(message=f'component request deleted-{branchRegion if compRequest.fault else userRegion}')
		print('end send_notification ##########')
		print('##################### end delete CompRequest ###########################')
		return Response({'msg': 'deleted successfully'}, status=status.HTTP_200_OK)
	return async_to_sync(deleteComponentRequest)()

@api_view(['GET',])
def approvedRequestComponent(request, pk=None):
	# this view is not currently in use
	if pk:
		async def approvedRequests():
			# get this pagiated data using getpagination custom hook
			user = await sync_to_async(User.objects.get)(pk=pk)
			print(f'user obj: {user}')
			approvedUser = await sync_to_async(lambda: list(RequestComponent.objects.filter(user=user, approved=True)))()
			# print(f'approvedUser: {approvedUser}')
			approvedUserRequestPaginator = PageNumberPagination()
			approvedUserRequestPaginator.page_size = 10  # Number of items per page
			paginatedRequest = approvedUserRequestPaginator.paginate_queryset(approvedUser, request)
			usererializer = await sync_to_async(lambda: RequestComponentReadSerializer(instance=paginatedRequest, many=True).data)()
			serialized_data = usererializer
			# print(f'usererializer: {usererializer.data}')
			return approvedUserRequestPaginator.get_paginated_response(serialized_data)
		return async_to_sync(approvedRequests)()

# ###################################
@api_view(['GET', 'POST', 'PATCH'])
def requestPart(request, pk=None, type=None):
	if request.method == 'POST':
		print(f'post payload: {request.data}')
		async def postPartRequest():
			# note: only workshop would not require fault field
			print('################# requestPart ####################')
			user = await sync_to_async(User.objects.select_related('region').get)(email=request.data['user'])
			region = user.region.name
			print(f'region:', region)
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
				requestSerializer = await sync_to_async(lambda: RequestPartCreateSerializer(data=cleanedData))()
				print(f'requestSerializer is valid: {await sync_to_async(requestSerializer.is_valid)()}')
				if await sync_to_async(requestSerializer.is_valid)():
					print(f'requestSerializer is valid')
					await sync_to_async(requestSerializer.save)()
					print(f'requestSerializer saved #################')
					print(f'requestSerializer saved instance: {requestSerializer.instance}')
					responseInstances.append(await sync_to_async(lambda: RequestPartReadSerializer(requestSerializer.instance).data)())
				else:
					print(f'requestSerializer error: {requestSerializer.errors}')
			print('################# end requestPart #################')
			response = 'Requests' if _ > 1 else f'{cleanedData["name"]} Request'
			print(f'length of requests: {_}')
			print(f'len responseInstances: {len(responseInstances)}')
			print(f'response: {response}')
			print('start send_notification ##########')
			await sync_to_async(send_notification)(message=f'make part request-{region}')
			print('end send_notification ##########')
			return Response({'msg': f'{response} Received.', 'responseObjs': responseInstances}, status=status.HTTP_200_OK)
		return async_to_sync(postPartRequest)()
	elif request.method == 'PATCH':
		async def patchPartRequests():
			# note: only workshop would not require fault field
			print('################# requestPart ####################')
			print(f'patch payload: {request.data}')
			partRequest = await sync_to_async(RequestPart.objects.select_related(
				'user__region', 'name'
			).get)(pk=request.data['requestID'])
			print(f'partRequest: {partRequest}')
			region = partRequest.user.region.name
			print(f'region: {region}')
			serializedPartRequest = await sync_to_async(lambda: RequestPartCreateSerializer(
				instance=partRequest, data=request.data, partial=True
			))()
			print(f'serializedPartRequest is valid: {await sync_to_async(serializedPartRequest.is_valid)()}')
			if await sync_to_async(serializedPartRequest.is_valid)():
				if request.data.get('approved'):
					partialData = {
						'name': partRequest.name.name,
						'quantity': partRequest.quantityRequested,
						'user': request.data['approved_by'],
					}
					UpdatePartSerializer = await sync_to_async(
					lambda: PartSerializer(
							data=partialData, context={'action': True}
						)
					)()
					print(f'is serializer valid:', await sync_to_async(UpdatePartSerializer.is_valid)())
					if await sync_to_async(UpdatePartSerializer.is_valid)():
						print(f'removing {partRequest.quantityRequested} items from {partRequest.name.name} in inventory')
						await sync_to_async(UpdatePartSerializer.save)()
				await sync_to_async(serializedPartRequest.save)()
				print(f'serializedPartRequest saved #################')
				print('start send_notification ##########')
				await sync_to_async(send_notification)(message=f'approve/reject part request-{region}')
				print('end send_notification ##########')
				return Response({'msg': 'Success'}, status=status.HTTP_200_OK)
			print(f'serializedPartRequest.error: {serializedPartRequest.errors}')
			return Response(serializedPartRequest.errors, status=status.HTTP_400_BAD_REQUEST)
		return async_to_sync(patchPartRequests)()
	elif request.method == 'GET':
		if pk:
			async def getPartRequest():
				# get this pagiated data using getpagination custom hook
				user = await sync_to_async(User.objects.get)(pk=pk)
				print(f'user obj: {user}')

				if user.role == 'workshop':
					partRequest = await sync_to_async(lambda: list(RequestPart.objects.filter(
					user=user, approved=False, rejected=False,
				)))()
				else:
					partRequest = await sync_to_async(lambda: list(RequestPart.objects.filter(
					user=user, approved=False, rejected=False,
					fault__confirm_resolve=False, fault__verify_resolve=False
				)))()
				print(f'user request: {partRequest}')

				partSerializer = await sync_to_async(lambda: RequestPartReadSerializer(instance=partRequest, many=True).data)()
				for part in partSerializer:
					part['type'] = 'part'
				# print(f'user: {user}')
				return partSerializer
			partSerializer = async_to_sync(getPartRequest)()
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
	async def getTotalPendingRequestPart():
		print('##################### total partRequests ###########################')
		user = await sync_to_async(User.objects.get)(pk=pk)
		if user.role == 'workshop':
				partRequests = await sync_to_async(lambda: list(RequestPart.objects.filter(
				user=user, approved=False, rejected=False,
			)))()
		else:
			partRequests = await sync_to_async(lambda: list(RequestPart.objects.filter(
				user=user, approved=False, rejected=False,
				fault__confirm_resolve=False, fault__verify_resolve=False
			)))()
		print(f'partRequests: {len(partRequests)}')
		print('##################### end total partRequests ###########################')
		return Response({'total': len(partRequests)}, status=status.HTTP_200_OK)
	return async_to_sync(getTotalPendingRequestPart)()

@api_view(['GET',])
def approvedRequestPart(request, pk=None):
	# this view is not currently in use
	if pk:
		async def approvedPartRequests():
			# get this pagiated data using getpagination custom hook
			user = await sync_to_async(User.objects.get)(pk=pk)
			print(f'user obj: {user}')
			approvedUser = await sync_to_async(lambda: list(RequestPart.objects.filter(user=user, approved=True)))()
			# print(f'approvedUser: {approvedUser}')
			approvedUserRequestPaginator = PageNumberPagination()
			approvedUserRequestPaginator.page_size = 10  # Number of items per page
			paginatedRequest = approvedUserRequestPaginator.paginate_queryset(approvedUser, request)
			usererializer = await sync_to_async(lambda: RequestPartReadSerializer(instance=paginatedRequest, many=True).data)()
			serialized_data = usererializer
			# print(f'usererializer: {usererializer.data}')
			return approvedUserRequestPaginator.get_paginated_response(serialized_data)
		return async_to_sync(approvedPartRequests)()

@api_view(['DELETE',])
def deletePartRequest(request, pk=None):
	# consider sending the pk of the user making the request to use in filtering the
	# select related db hit
	async def deletePartzRequest():
		print('##################### delete partRequest ###########################')
		print(f'deleting ... ❌❌')
		branchRegion = None
		try:
			partRequest = await sync_to_async(RequestPart.objects.select_related(
				'user__region', 'fault__logged_by__branch__region'
			).get)(pk=pk)
			branchRegion = partRequest.fault.logged_by.branch.region.name
			print(f'branchRegion: {branchRegion}')
		except AttributeError:
			partRequest = await sync_to_async(RequestPart.objects.select_related(
				'user__region'
			).get)(pk=pk)
		except:
			return Response({'error': 'partRequest not found'}, status=status.HTTP_404_NOT_FOUND)
		print(f'partRequest: {partRequest}')
		userRegion = partRequest.user.region.name
		print(f'userRegion: {userRegion}')
		await sync_to_async(partRequest.delete)()
		print(f'done ✅✅✅')
		print('start send_notification ##########')
		await sync_to_async(send_notification)(message=f'part request deleted-{branchRegion if partRequest.fault else userRegion}')
		print('end send_notification ##########')
		print('##################### end delete partRequest ###########################')
		return Response({'msg': 'deleted successfully'}, status=status.HTTP_200_OK)
	return async_to_sync(deletePartzRequest)()

###################################################
@api_view(['GET'])
def regionUserRequests(request, pk=None, type=None):
	async def getRegionUserRequests():
		print('##################### regionUserRequests ###########################')
		# Get the help-desk user
		user = await sync_to_async(User.objects.select_related('region').get)(pk=pk)
		# get the region of the help-desk
		region = user.region
		print(f'help-desk/supervisor: {user}')
		print(f'region: {region.name}')
		print()

		################ efficient code ########################
		# Fetch the unresolved faults queryset once
		unresolved_faults_queryset = await sync_to_async(lambda: Fault.objects.filter(
			verify_resolve=False,
			confirm_resolve=False
		).prefetch_related('partfault', 'componentfault'))()
		faults_with_requests = unresolved_faults_queryset.filter(
			# At least one type of request exists
			Q(partfault__isnull=False) | Q(componentfault__isnull=False),
			Q(partfault__approved=False) & Q(partfault__rejected=False),
			Q(componentfault__approved=False) & Q(componentfault__rejected=False)
		).distinct()

		engineers = await sync_to_async(lambda: list(User.objects.filter(
			Q(role='engineer') | Q(role='supervisor'),
			region=region,
			assignedto__in=faults_with_requests
		).prefetch_related(
			Prefetch(
				'assignedto',
				queryset=faults_with_requests,
				to_attr='unresolved_faults'
			)
		).distinct()))()

		# allFaultsData = []  # Store all faults for all engineers
		allEngineersData = []  # Store all faults for all engineers
		# loop through retrieved engineers objects
		for eIndex, engineer in enumerate(engineers):
			# ascertain if current engineer has parts/components requests
			engineerSerializer = await sync_to_async(lambda: UserReadHandlersSerializer(instance=engineer).data)()
			partRequestExist = any([await sync_to_async(fault.partfault.exists)() for fault in engineer.unresolved_faults])
			componentRequestExist = any([await sync_to_async(fault.componentfault.exists)() for fault in engineer.unresolved_faults])
			# print(f'comp: {componentRequestExist}, part: {partRequestExist}')
			print(f'{eIndex+1}. engineer: {engineer.first_name} - has requests: {partRequestExist or componentRequestExist}')

			for fault in engineer.unresolved_faults:
				print(f'	faultID: {fault.id} verified: {fault.verify_resolve}, confirmed: {fault.confirm_resolve}')
				for compReq in await sync_to_async(lambda: list(fault.componentfault.all()))():
					# if not (compReq.approved or compReq.rejected):
					print(f'		compID: {compReq.id} approved/rejected: {compReq.approved or compReq.rejected}')
				for partReq in await sync_to_async(lambda: list(fault.partfault.all()))():
					# if not (partReq.approved or partReq.rejected):
					print(f'		partID: {partReq.id} approved/rejected: {partReq.approved or partReq.rejected}')
			# print(f'part requests: {[f"faultID {fault.id}: {[part.id for part in await sync_to_async(lambda: list(fault.partfault.all()))()]}" for fault in engineer.unresolved_faults if partRequestExist]}')
			faultInstances = [fault for fault in engineer.unresolved_faults if (partRequestExist or componentRequestExist)]
			faultSerializer = await sync_to_async(lambda: FaultReadSerializer(
				instance=faultInstances,
				many=True
			).data)()
			# print(f'	faults: {[fault["id"] for fault in faultSerializer]}')
			# print(f'	faults: {[f"{fault.id} => confirm: {fault.confirm_resolve}" for fault in engineer.unresolved_faults]}')

			# Attach additional data to each fault
			for faultData, faultInstance in zip(faultSerializer, faultInstances):
				faultCompRequests = await sync_to_async(lambda: list(faultInstance.componentfault.all()))()
				faultPartRequests = await sync_to_async(lambda: list(faultInstance.partfault.all()))()
				# print(f'		fault: {faultInstance.id}')
				# print(f'		compRequests: {[comp.id for comp in faultCompRequests]}, partrequest: {[part.id for  part in faultPartRequests]}')
				# print(f'faultCompRequests before: {faultCompRequests}')
				# print(f'length: {len(faultCompRequests)}')
				# print('\n')
				##############################################################
				##############################################################
				##############################################################
				##############################################################
				if not faultCompRequests and not faultPartRequests: continue
				##############################################################
				##############################################################
				##############################################################
				##############################################################
				# print(f'faultCompRequests after: {faultCompRequests}')
				# print(f'length: {len(faultCompRequests)}')
				# print(f'fault name: {faultInstance.title}, {faultInstance.id}')
				# print('\n')
				# print(f'	serializing fault: {faultInstance.id} #############')

				# Serialize component and part requests
				compRequestSerializer = await sync_to_async(lambda: RequestFaultComponentReadSerializer(faultCompRequests, many=True).data)()
				partRequestSerializer = await sync_to_async(lambda: RequestFaultPartReadSerializer(faultPartRequests, many=True).data)()

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
		return allEngineersData
	allEngineersData = async_to_sync(getRegionUserRequests)()

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
	async def getTotalRegionUserRequests():
		print('##################### total totalRegionUserRequests ###########################')
		helpdesk = await sync_to_async(User.objects.select_related('region').get)(pk=pk)
		print(f'help-desk (totalRegionUserRequests): {helpdesk}')
		region = helpdesk.region
		print(f'region: {region.name}')
		# Fetch the unresolved faults queryset once
		unresolved_faults_queryset = await sync_to_async(lambda: Fault.objects.filter(
			verify_resolve=False,
			confirm_resolve=False
		).prefetch_related('partfault', 'componentfault'))()
		faults_with_requests = unresolved_faults_queryset.filter(
			# At least one type of request exists
			Q(partfault__isnull=False) | Q(componentfault__isnull=False),
			Q(partfault__approved=False) & Q(partfault__rejected=False),
			Q(componentfault__approved=False) & Q(componentfault__rejected=False)
		).distinct()

		engineers = await sync_to_async(lambda: list(User.objects.filter(
			Q(role='engineer') | Q(role='supervisor'),
			region=region,
			assignedto__in=faults_with_requests
		).prefetch_related(
			Prefetch(
				'assignedto',
				queryset=faults_with_requests,
				to_attr='unresolved_faults'
			)
		).distinct()))()

		print(f'engineers: {engineers}')
		print(f'total count: {len(engineers)}')
		print('##################### end total totalRegionUserRequests ###########################')
		return Response({'total': len(engineers)}, status=status.HTTP_200_OK)
	return async_to_sync(getTotalRegionUserRequests)()

###################################################
@api_view(['GET'])
def unconfirmedRegionResolutions(request, pk=None, type=None):
	async def getRegionUnconfirmedResolutions():
		print('##################### unconfirmedRegionResolutions ###########################')
		user = await sync_to_async(User.objects.select_related('region').get)(pk=pk)
		region = user.region
		print(f'help-desk user: {user}')
		print(f'region: {region.name}')

		# Fetch all engineers from the same region
		engineers = await sync_to_async(lambda: list(User.objects.filter(
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
		).distinct()))()
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

			engineerSerializer = await sync_to_async(lambda: UserReadHandlersSerializer(instance=engineer).data)()
			partRequest = any([await sync_to_async(fault.partfault.exists)() for fault in engineer.unresolved_faults])
			componentRequest = any([await sync_to_async(fault.componentfault.exists)() for fault in engineer.unresolved_faults])
			print(f'{eIndex+1}. engineer: {engineer.first_name} - has requests: {partRequest or componentRequest}')
			faultInstances = engineer.unresolved_faults
			print(f'	component requests: {[f"faultID {fault.id}: {[comp.id for comp in fault.componentfault.all()]}" for fault in engineer.unresolved_faults if fault.componentfault.exists()]}')
			print(f'	part requests: {[f"faultID {fault.id}: {[part.id for part in fault.partfault.all()]}" for fault in engineer.unresolved_faults if fault.partfault.exists()]}')
			count += len(faultInstances)
			faultSerializer = await sync_to_async(lambda: FaultReadSerializer(faultInstances, many=True).data)()
			print(f'		faults: {[fault.id for fault in faultInstances]}')
			# print(f'			faults: {[f"{fault.id}, verified: {fault.verify_resolve}, confirm: {fault.confirm_resolve}" for fault in faultInstances]}')
			# print(f'			faults: {[f"{fault.id}, confirm: {fault.confirm_resolve}" for fault in faultInstances]}')
			# serializedFaults = faultSerializer.data
			print()
			for faultData, faultInstance in zip(faultSerializer, faultInstances):
				# if faultInstance.componentfault.exists() or faultInstance.partfault.exists():
				faultCompRequests = await sync_to_async(lambda: list(faultInstance.componentfault.all()))()
				faultPartRequests = await sync_to_async(lambda: list(faultInstance.partfault.all()))()

				# Serialize component and part requests
				compRequestSerializer = await sync_to_async(lambda: RequestFaultComponentReadSerializer(faultCompRequests, many=True).data)()
				partRequestSerializer = await sync_to_async(lambda: RequestFaultPartReadSerializer(faultPartRequests, many=True).data)()

				# Add the serialized requests to the fault data
				faultData['requestComponent'] = compRequestSerializer if compRequestSerializer else False
				faultData['requestPart'] = partRequestSerializer if partRequestSerializer else False
				faultData['requestStatus'] = bool(compRequestSerializer) or bool(partRequestSerializer)

			engineerSerializer['faults'] = faultSerializer if faultSerializer else False

			# Add this fault to the overall list
			allEngineersData.append(engineerSerializer)
		print(f'total faults: {count}')
		print('##################### end UUUUUUUUUUUUUUUU ###########################')
		return allEngineersData
	allEngineersData = async_to_sync(getRegionUnconfirmedResolutions)()
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
	async def getTotalUnconfirmedRegionResolutions():
		print('##################### total totalUnconfirmedRegionResolutions ###########################')
		helpdesk = await sync_to_async(User.objects.select_related('region').get)(pk=pk)
		print(f'help-desk (totalUnconfirmedRegionResolutions): {helpdesk}')
		region = helpdesk.region
		print(f'region: {region.name}')
		engineers = await sync_to_async(lambda: list(User.objects.filter(
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
		).distinct()))()
		print(f'Engineers length: {len(engineers)}')
		engineers = list(filter(lambda engineer: engineer.unresolved_faults != [], engineers))
		print(f'engineers: {engineers}')
		print(f'total count: {len(engineers)}')
		print('##################### end total totalUnconfirmedRegionResolutions ###########################')
		return Response({'total': len(engineers)}, status=status.HTTP_200_OK)
	return async_to_sync(getTotalUnconfirmedRegionResolutions)()

@api_view(['PATCH'])
def requestStatus(request, pk=None):
	if request.method == 'PATCH':
		async def patchRequestStatus():
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
			compSerializer = None
			partSerializer = None
			region = None
			if 'requestComponentIds' in requestList:
				for compRequestID in request.data['requestComponentIds'].split(','):
					print(f'compRequestID: {compRequestID}')
					compRequestInstance = await sync_to_async(RequestComponent.objects.select_related(
						'fault__logged_by__branch__region', 'name'
					).get)(pk=compRequestID)
					region = compRequestInstance.fault.logged_by.branch.region
					# print(f'approved: {compRequestInstance.approved}, rejected: {compRequestInstance.rejected}')
					if compRequestInstance.approved or compRequestInstance.rejected:
						print(f'Request component {compRequestID} has already been responded to. Skipping...')
						continue
					# print(f'status: {compRequestInstance.approved or compRequestInstance.rejected}')
					compSerializer = await sync_to_async(lambda: RequestComponentUpdateSerializer(instance=compRequestInstance, data=cleanedData, partial=True))()
					print(f'compSerializer is valid: {await sync_to_async(compSerializer.is_valid)()}')
					if await sync_to_async(compSerializer.is_valid)():
						if 'approved' in requestList:
							partialData = {
								'name': compRequestInstance.name.name,
								'quantity': compRequestInstance.quantityRequested,
								'user': cleanedData['approved_by'],
							}
							UpdateComponentSerializer = await sync_to_async(
							lambda: ComponentSerializer(
									data=partialData, context={'action': True}
								)
							)()
							print(f'is serializer valid:', await sync_to_async(UpdateComponentSerializer.is_valid)())
							if await sync_to_async(UpdateComponentSerializer.is_valid)():
								print(f'removing {compRequestInstance.quantityRequested} items from {compRequestInstance.name.name} in inventory')
								await sync_to_async(UpdateComponentSerializer.save)()
						await sync_to_async(compSerializer.save)()
						print(f'compSerializer for request {compRequestID} is saved successfully. ##################')
					print(f'compserializer error: {compSerializer.errors}')
					# print()
			# return Response({'allgood'})
			if 'requestPartIDs' in requestList:
				for partRequestID in request.data['requestPartIDs'].split(','):
					partRequestInstance = await sync_to_async(RequestPart.objects.select_related(
						'fault__logged_by__branch__region', 'name'
					).get)(pk=partRequestID)
					region = partRequestInstance.fault.logged_by.branch.region
					if partRequestInstance.approved or partRequestInstance.rejected:
						print(f'Request part {partRequestID} has already been responded to. Skipping...')
						continue
					partSerializer = await sync_to_async(lambda: RequestPartUpdateSerializer(instance=partRequestInstance, data=cleanedData, partial=True))()
					print(f'partSerializer is valid: {await sync_to_async(partSerializer.is_valid)()}')
					if await sync_to_async(partSerializer.is_valid)():
						if 'approved' in requestList:
							partialData = {
								'name': partRequestInstance.name.name,
								'quantity': partRequestInstance.quantityRequested,
								'user': cleanedData['approved_by'],
							}
							UpdatePartSerializer = await sync_to_async(
							lambda: PartSerializer(
									data=partialData, context={'action': True}
								)
							)()
							print(f'is serializer valid:', await sync_to_async(UpdatePartSerializer.is_valid)())
							if await sync_to_async(UpdatePartSerializer.is_valid)():
								print(f'removing {partRequestInstance.quantityRequested} items from {partRequestInstance.name.name} in inventory')
								await sync_to_async(UpdatePartSerializer.save)()
						await sync_to_async(partSerializer.save)()
						print(f'partSerializer for request {partRequestID} is saved successfully. ##################')
					print(f'partSerializer error: {partSerializer.errors}')
			if compSerializer or partSerializer:
				print('start send_notification ##########')
				await sync_to_async(send_notification)(message=f'approve/reject components and/or parts request-{region.name}')
				print('end send_notification ##########')
				return Response({'msg': 'success'}, status=status.HTTP_200_OK)
			else:
				return Response({'msg': 'Request has initially been responded to'}, status=status.HTTP_200_OK)
		return async_to_sync(patchRequestStatus)()
	return Response({'wrong method used'}, status=status.HTTP_200_OK)

###################################################
@api_view(['GET'])
def faultsWithRequests(request, pk=None):
	async def getFaultsWithRequests():
		print('##################### faultsWithRequests ###########################')
		# fetch users who are engineers, have unconfirmed faults and have part/component (or both) requests
		# engineers = await sync_to_async(lambda: list(User.objects.filter(
		# 	role='engineer'  # Fetch users who are engineers
		# ).filter(
		# 	Q(assignedto__isnull=False) &  # Ensure the engineer has assigned faults
		# 	(
		# 		Q(assignedto__partfault__isnull=False) |  # Faults with part requests
		# 		Q(assignedto__componentfault__isnull=False)  # Faults with component requests
		# 	) & (
		# 		# Part fault conditions
		# 		(
		# 			Q(assignedto__partfault__approved=False) &
		# 			Q(assignedto__partfault__rejected=False)
		# 		) |
		# 		# Component fault conditions
		# 		(
		# 			Q(assignedto__componentfault__approved=False) &
		# 			Q(assignedto__componentfault__rejected=False)
		# 		)
		# 	)
		# ).prefetch_related(
		# 	'assignedto__partfault',  # Fetch related part requests
		# 	'assignedto__componentfault'  # Fetch related component requests
		# ).distinct()))()  # Prevent duplicates

		unresolved_faults_queryset = await sync_to_async(lambda: Fault.objects.filter(
			verify_resolve=False,
			confirm_resolve=False
		).prefetch_related('partfault', 'componentfault'))()
		faults_with_requests = unresolved_faults_queryset.filter(
			# At least one type of request exists
			Q(partfault__isnull=False) | Q(componentfault__isnull=False),
			Q(partfault__approved=False) & Q(partfault__rejected=False),
			Q(componentfault__approved=False) & Q(componentfault__rejected=False)
		).distinct()

		engineers = await sync_to_async(lambda: list(User.objects.filter(
			Q(role='engineer') | Q(role='supervisor'),
			assignedto__in=faults_with_requests
		).prefetch_related(
			Prefetch(
				'assignedto',
				queryset=faults_with_requests,
				to_attr='unresolved_faults'
			)
		).distinct()))()

		allFaultsData = []  # Store all faults for all engineers

		countVerified = 0
		countUnverified = 0
		totalVerified = 0
		# countUnresolved = 0
		# loop through retrieved engineers objects
		for eIndex, engineer in enumerate(engineers):
			# ascertain if current engineer has parts/components requests
			engineerSerializer = await sync_to_async(lambda: UserReadHandlersSerializer(instance=engineer).data)()
			partRequestExist = any([await sync_to_async(fault.partfault.exists)() for fault in engineer.unresolved_faults])
			componentRequestExist = any([await sync_to_async(fault.componentfault.exists)() for fault in engineer.unresolved_faults])
			# print(f'comp: {componentRequestExist}, part: {partRequestExist}')
			print(f'{eIndex+1}. engineer: {engineer.first_name} - has requests: {partRequestExist or componentRequestExist}')

			# checks if engineer has faults and requests
			for fault in engineer.unresolved_faults:
				print(f'	faultID: {fault.id} verified: {fault.verify_resolve}, confirmed: {fault.confirm_resolve}')
				for compReq in await sync_to_async(lambda: list(fault.componentfault.all()))():
					# if not (compReq.approved or compReq.rejected):
					print(f'		compID: {compReq.id} approved/rejected: {compReq.approved or compReq.rejected}')
				for partReq in await sync_to_async(lambda: list(fault.partfault.all()))():
					# if not (partReq.approved or partReq.rejected):
					print(f'		partID: {partReq.id} approved/rejected: {partReq.approved or partReq.rejected}')

			faultInstances = [fault for fault in engineer.unresolved_faults if (partRequestExist or componentRequestExist)]
			faultSerializer = await sync_to_async(lambda: FaultReadSerializer(
				instance=faultInstances,
				many=True
			).data)()

			for faultData, faultInstance in zip(faultSerializer, faultInstances):
				faultCompRequests = await sync_to_async(lambda: list(faultInstance.componentfault.all()))()
				faultPartRequests = await sync_to_async(lambda: list(faultInstance.partfault.all()))()

				if not faultCompRequests and not faultPartRequests: continue

				compRequestSerializer = await sync_to_async(lambda: RequestFaultComponentReadSerializer(faultCompRequests, many=True).data)()
				partRequestSerializer = await sync_to_async(lambda: RequestFaultPartReadSerializer(faultPartRequests, many=True).data)()

				# Add the serialized requests to the fault data
				faultData['requestComponent'] = compRequestSerializer if compRequestSerializer else False
				faultData['requestPart'] = partRequestSerializer if partRequestSerializer else False
				faultData['requestStatus'] = bool(compRequestSerializer) or bool(partRequestSerializer)
				faultData['engineer'] = engineerSerializer
			# engineerSerializer['faults'] = faultSerializer if faultSerializer else False

			# Add this fault to the overall list
			allFaultsData.append(faultData)

		# print(f'fault instances: {len(faultInstances)}')
		print()
		print(f'verified: {countVerified}')
		print(f'unverified: {countUnverified}')
		# print(f'countUnresolved: {countUnresolved}')
		print(f'total: {totalVerified}')
		return allFaultsData
	allFaultsData = async_to_sync(getFaultsWithRequests)()

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
	async def getTotalFaultsWithRequests():
		print('##################### total totalFaultsWithRequests ###########################')
		unresolved_faults_queryset = await sync_to_async(lambda: Fault.objects.filter(
			verify_resolve=False,
			confirm_resolve=False
		).prefetch_related('partfault', 'componentfault'))()
		faults_with_requests = unresolved_faults_queryset.filter(
			# At least one type of request exists
			Q(partfault__isnull=False) | Q(componentfault__isnull=False),
			Q(partfault__approved=False) & Q(partfault__rejected=False),
			Q(componentfault__approved=False) & Q(componentfault__rejected=False)
		).distinct()

		engineers = await sync_to_async(lambda: list(User.objects.filter(
			Q(role='engineer') | Q(role='supervisor'),
			assignedto__in=faults_with_requests
		).prefetch_related(
			Prefetch(
				'assignedto',
				queryset=faults_with_requests,
				to_attr='unresolved_faults'
			)
		).distinct()))()

		print(f'engineers: {engineers}')
		print(f'length: {len(engineers)}')
		print('##################### end total totalFaultsWithRequests ###########################')
		return Response({'total': len(engineers)}, status=status.HTTP_200_OK)
	return async_to_sync(getTotalFaultsWithRequests)()

@api_view(['GET'])
def unapprovedWorkshopRequests(request, pk=None, type=None):
	async def getUnapprovedWorkshopRequests():
		print('################# user unapprovedWorkshopRequests #################')
		print(f'request type: {request.method}')
		print(f'pk: {pk}')
		# if request.method == 'GET':
		unconfirmedFixedPart = UnconfirmedPart.objects.filter(approved=False, rejected=False)
		componentRequests = RequestComponent.objects.filter(approved=False, rejected=False)
		user = await sync_to_async(lambda: User.objects.prefetch_related(
			Prefetch(
				'partpostedby',  # The related name for the ForeignKey
				queryset=unconfirmedFixedPart,  # Apply filtering
				to_attr='filtered_parts'  # Store the filtered related objects in this attribute
			),
			Prefetch(
				'componentrequestuser',  # The related name for the ForeignKey
				queryset=componentRequests,  # Apply filtering
				to_attr='filtered_components'  # Store the filtered related objects in this attribute
			)
		).get(pk=pk))()
		print(f'user: {user}')
		# print(f'user: {user}')
		unapprovedPart = user.filtered_parts
		unapprovedComponent = user.filtered_components
		combinedLists = user.filtered_components + user.filtered_parts
		print(f'combined ids: {[comb.id for comb in combinedLists]}')
		print(f'posted parts ids: {[part.id for part in unapprovedPart]}')
		print(f'component ids: {[component.id for component in unapprovedComponent]}')

		componentSerializer = await sync_to_async(lambda: RequestComponentReadSerializer(instance=unapprovedComponent, many=True).data)()
		for comp in componentSerializer:
			comp['type'] = 'component'
		partSerializer = await sync_to_async(lambda: UnconfirmedPartSerializer(instance=unapprovedPart, many=True).data)()
		for part in partSerializer:
			part['type'] = 'part'
		combinedSerializedItems = componentSerializer + partSerializer
		return combinedSerializedItems
	combinedSerializedItems = async_to_sync(getUnapprovedWorkshopRequests)()
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

####################################################################
########### hr #####################
@api_view(['GET'])
def allUserRequests(request, pk=None, type=None):
	async def getAllUserRequests():
		print('##################### regionUserRequests ###########################')
		# Get the help-desk user
		user = await sync_to_async(User.objects.get)(pk=pk)
		# get the region of the help-desk
		role = user.role
		print(f'human-resource: {user}')
		print(f'role: {role}')
		print()

		################ efficient code ########################
		# Fetch the unresolved faults queryset once
		unresolved_faults_queryset = await sync_to_async(lambda: Fault.objects.filter(
			verify_resolve=False,
			confirm_resolve=False
		).prefetch_related('partfault', 'componentfault'))()
		faults_with_requests = unresolved_faults_queryset.filter(
			# At least one type of request exists
			Q(partfault__isnull=False) | Q(componentfault__isnull=False),
			Q(partfault__approved=False) & Q(partfault__rejected=False),
			Q(componentfault__approved=False) & Q(componentfault__rejected=False)
		).distinct()

		engineers = await sync_to_async(lambda: list(User.objects.filter(
			Q(role='engineer') | Q(role='supervisor'),
			assignedto__in=faults_with_requests
		).prefetch_related(
			Prefetch(
				'assignedto',
				queryset=faults_with_requests,
				to_attr='unresolved_faults'
			)
		).distinct()))()

		# print(f'engineers: {engineers}')

		# allFaultsData = []  # Store all faults for all engineers
		allEngineersData = []  # Store all faults for all engineers

		# loop through retrieved engineers objects
		for eIndex, engineer in enumerate(engineers):
			# ascertain if current engineer has parts/components requests
			engineerSerializer = await sync_to_async(lambda: UserReadHandlersSerializer(instance=engineer).data)()
			partRequestExist = any([await sync_to_async(fault.partfault.exists)() for fault in engineer.unresolved_faults])
			componentRequestExist = any([await sync_to_async(fault.componentfault.exists)() for fault in engineer.unresolved_faults])
			# print(f'comp: {componentRequestExist}, part: {partRequestExist}')
			print(f'{eIndex+1}. engineer: {engineer.first_name} - has requests: {partRequestExist or componentRequestExist}')

			# checks if engineer has faults and requests
			for fault in engineer.unresolved_faults:
				print(f'	faultID: {fault.id} verified: {fault.verify_resolve}, confirmed: {fault.confirm_resolve}')
				for compReq in await sync_to_async(lambda: list(fault.componentfault.all()))():
					# if not (compReq.approved or compReq.rejected):
					print(f'		compID: {compReq.id} approved/rejected: {compReq.approved or compReq.rejected}')
				for partReq in await sync_to_async(lambda: list(fault.partfault.all()))():
					# if not (partReq.approved or partReq.rejected):
					print(f'		partID: {partReq.id} approved/rejected: {partReq.approved or partReq.rejected}')

			faultInstances = [fault for fault in engineer.unresolved_faults if (partRequestExist or componentRequestExist)]
			faultSerializer = await sync_to_async(lambda: FaultReadSerializer(
				instance=faultInstances,
				many=True
			).data)()

			# print()
			# Attach additional data to each fault
			for faultData, faultInstance in zip(faultSerializer, faultInstances):
				faultCompRequests = await sync_to_async(lambda: list(faultInstance.componentfault.all()))()
				faultPartRequests = await sync_to_async(lambda: list(faultInstance.partfault.all()))()

				if not faultCompRequests and not faultPartRequests: continue

				# Serialize component and part requests
				compRequestSerializer = await sync_to_async(lambda: RequestFaultComponentReadSerializer(faultCompRequests, many=True).data)()
				for component in compRequestSerializer:
					component['type'] = 'component'
				partRequestSerializer = await sync_to_async(lambda: RequestFaultPartReadSerializer(faultPartRequests, many=True).data)()
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
		return allEngineersData
	allEngineersData = async_to_sync(getAllUserRequests)()
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
	async def getAllTotalUserRequests():
		print('##################### total totalRegionUserRequests ###########################')
		helpdesk = await sync_to_async(User.objects.select_related('region').get)(pk=pk)
		print(f'help-desk (totalRegionUserRequests): {helpdesk}')
		region = helpdesk.region
		print(f'region: {region.name}')

		# Fetch the unresolved faults queryset once
		unresolved_faults_queryset = await sync_to_async(lambda: Fault.objects.filter(
			verify_resolve=False,
			confirm_resolve=False
		).prefetch_related('partfault', 'componentfault'))()
		faults_with_requests = unresolved_faults_queryset.filter(
			# At least one type of request exists
			Q(partfault__isnull=False) | Q(componentfault__isnull=False),
			Q(partfault__approved=False) & Q(partfault__rejected=False),
			Q(componentfault__approved=False) & Q(componentfault__rejected=False)
		).distinct()

		engineers = await sync_to_async(lambda: list(User.objects.filter(
			Q(role='engineer') | Q(role='supervisor'),
			assignedto__in=faults_with_requests
		).prefetch_related(
			Prefetch(
				'assignedto',
				queryset=faults_with_requests,
				to_attr='unresolved_faults'
			)
		).distinct()))()

		# print(f'engineers: {engineers}')
		print(f'engineers: {engineers}')
		print(f'total count: {len(engineers)}')
		print('##################### end total totalRegionUserRequests ###########################')
		return Response({'total': len(engineers)}, status=status.HTTP_200_OK)
	return async_to_sync(getAllTotalUserRequests)()

@api_view(['GET'])
def workshopRequests(request, pk=None, type=None):
	async def getAllWorkshopRequests():
		print('##################### workshopRequests ###########################')
		user = await sync_to_async(User.objects.get)(pk=pk)
		print(f'user: {user}')
		componentRequests = await sync_to_async(lambda: list(RequestComponent.objects.select_related(
			'user'
		).filter(
			# user=user,
			user__role='workshop',
			approved=False,
			rejected=False
		)))()
		[print(f'componentID: {component.id}, approved: {component.approved}, rejected: {component.rejected}, dept: {component.user.role}, user: {component.user.first_name}') for component in componentRequests]
		# return Response({'allgood'})
		serializedComponents = await sync_to_async(lambda: RequestComponentReadSerializer(instance=componentRequests, many=True).data)()
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
	return async_to_sync(getAllWorkshopRequests)()

@api_view(['GET'])
def totalWorkshopRequests(request, pk=None, type=None):
	async def getTotalWorkshopRequests():
		print('##################### totalWorkshopRequests ###########################')
		user = await sync_to_async(User.objects.get)(pk=pk)
		print(f'user: {user}')
		componentRequests = await sync_to_async(lambda: list(RequestComponent.objects.filter(
			# user=user,
			user__role='workshop',
			approved=False,
			rejected=False
		)))()
		total = len(componentRequests)
		print(f'total: {total}')
		# print(f'total count: {len(engineers)}')
		print('##################### end totalWorkshopRequests ###########################')
		return Response({'total': total}, status=status.HTTP_200_OK)
	return async_to_sync(getTotalWorkshopRequests)()

@api_view(['GET'])
def allRequestsOnly(request, pk=None, type=None):
	async def getAllRequestsOnly():
		print('################# allRequestsOnly #################')
		print(f'request type: {request.method}')
		print(f'pk: {pk}')
		user = await sync_to_async(User.objects.get)(pk=pk)
		partRequests = await sync_to_async(lambda: list(RequestPart.objects.select_related(
			'fault', 'user'
		).filter(
				Q(fault__isnull=True) |
				(Q(fault__confirm_resolve=False) &	Q(fault__verify_resolve=False)
			),
			approved=False,
			rejected=False
		)))()
		componentRequests = await sync_to_async(lambda: list(RequestComponent.objects.select_related(
			'fault', 'user'
		).filter(
				Q(fault__isnull=True) |
				(Q(fault__confirm_resolve=False) &	Q(fault__verify_resolve=False)
			),
			approved=False,
			rejected=False
		)))()
		fixedParts = await sync_to_async(lambda: list(UnconfirmedPart.objects.select_related(
			'user'
		).filter(
			approved=False,
			rejected=False
		)))()
		print(f'user: {user}')
		print()
		print(f'components >>>>>>>>>>')
		for comp in componentRequests:
			print(f'componentID: {comp.id}, approved: {comp.approved}, rejected: {comp.rejected}')
			if comp.fault:
				print(f'faultID: {comp.fault.id}, verify_resolve: {comp.fault.verify_resolve}, confirm_resolve: {comp.fault.confirm_resolve}')
			else: print('no fault ######')
			print(f'user: {comp.user.first_name}')
			print()
		print()
		print(f'parts >>>>>>>>>>')
		for part in partRequests:
			print(f'partID: {part.id}, approved: {part.approved}, rejected: {part.rejected}')
			if part.fault:
				print(f'faultID: {part.fault.id}, verify_resolve: {part.fault.verify_resolve}, confirm_resolve: {part.fault.confirm_resolve}')
			else: print('no fault ######')
			print(f'user: {part.user.first_name}')
			print()
		print()
		print(f'fixed parts >>>>>>>>>>')
		for fpart in fixedParts:
			print(f'partID: {fpart.id}, approved: {fpart.approved}, rejected: {fpart.rejected}')
			print(f'user: {fpart.user.first_name}')
			print()

		componentSerializer = await sync_to_async(lambda: RequestComponentReadSerializer(instance=componentRequests, many=True).data)()
		for comp in componentSerializer:
			comp['type'] = 'component'
		partSerializer = await sync_to_async(lambda: RequestPartReadSerializer(instance=partRequests, many=True).data)()
		for part in partSerializer:
			part['type'] = 'part'
		fixedPartsSerializer = await sync_to_async(lambda: UnconfirmedPartSerializer(instance=fixedParts, many=True).data)()
		for fixedPart in fixedPartsSerializer:
			fixedPart['type'] = 'fixed-part'
		combinedSerializedItems = componentSerializer + partSerializer + fixedPartsSerializer
		return combinedSerializedItems
	combinedSerializedItems = async_to_sync(getAllRequestsOnly)()
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
