from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from app_deliveries.models import Deliveries
from app_deliveries.serializers import UserDeliveriesSerializer
from app_users.models import Region
from app_bank.models import *
from app_bank.serializers import *
from app_location.models import Location
from app_custodian.models import Custodian
from app_inventory.serializers import RequestFaultComponentReadSerializer, RequestFaultPartReadSerializer
from .serializers import *
from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime
from app_sse_notification.firebase_utils import send_notification
# from app_sse_notification.utils import send_notification
from asgiref.sync import sync_to_async, async_to_sync
from django.http import JsonResponse

def compartmentalizedList(listValue: list):
	newDict = {}
	for item in listValue:
		_, id = item.split('-')
		if id not in newDict:
			newDict[id] = []
		newDict[id].append(item)
	return newDict

# Create your views here.
@api_view(['GET',])
def faultName(request, pk=None):
	async def getData():
		faultNames = await sync_to_async(FaultName.objects.all)()
		# print(f'faultNames: {faultNames}')
		serializer = await sync_to_async(lambda: FaultNameSerializer(faultNames, many=True).data)()
		print(f'faultNames serialized: {serializer}')
		return serializer
	serializer = async_to_sync(getData)()
	return Response(serializer, status=status.HTTP_200_OK)

@api_view(['GET',])
def faultDetail(request, pk=None):
	async def getData():
		faultObj = await sync_to_async(Fault.objects.get)(pk=pk)
		# print(f'faultObj: {faultObj}')
		serializer = await sync_to_async(lambda: FaultCreateUpdateSerializer(instance=faultObj).data)()
		print(f'faultObj serialized: {serializer}')
		return serializer
	serializer = async_to_sync(getData)()
	return Response(serializer, status=status.HTTP_200_OK)

@api_view(['POST'])
def fault(request, pk=None):
	if request.method == 'POST':
		print('fault payload:', request.data)
		async def postData():
			try:
				# Get region and location objects asynchronously
				region = await sync_to_async(Region.objects.get)(name=request.data['region'])
				locationName, locationID = request.data['location'].split('-')
				print(f'locationName: {locationName}')
				print(f'locationID: {locationID}')
				location = await sync_to_async(Location.objects.get)(id=int(locationID))
				# location = await sync_to_async(Location.objects.get)(id=locationID)
				print(f'location: {location.id}')
			except (KeyError, Region.DoesNotExist, Location.DoesNotExist) as e:
				print(f'error for region and location: {e}')
				return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
			dictionary = {item: request.data[item] for item in request.data}
			print(f'dictionary: {dictionary}')
			faultList = [i for i in request.data if i.startswith('fault') or i.startswith('other')]
			print(f'faultList: {faultList}')
			dictOfLists = compartmentalizedList(faultList)
			print(f'dictOfLists: {dictOfLists}')
			length = len(dictOfLists)

			# Validation for empty fault list
			if not faultList:
				return Response({'error': 'No faults provided'}, status=status.HTTP_400_BAD_REQUEST)

			try:
				print('try block')
				dicttn = {}
				# Process each fault asynchronously
				for item in dictOfLists.values():
					print(f'item:', item)
					dicttn['title'] = request.data[item[0]]
					if len(item) > 1:
						dicttn['other'] = request.data[item[1]]
					else:
						dicttn['other'] = None
					dicttn.update({item: request.data[item] for item in list(request.data)})
					dicttn['location'] = location.id
					print(f'new dicttn:', dicttn)

					# Wrap serializer operations in sync_to_async
					print('before serializer')
					serializer = await sync_to_async(lambda: FaultCreateUpdateSerializer(data=dicttn))()
					print('after serializer')
					if await sync_to_async(serializer.is_valid)():
						print('before serializer save')
						length -= 1
						await sync_to_async(serializer.save)()
						print(f'saved: {dicttn}')
						print(f'SAVED #########################')
						if length != 0:
							continue
					else:
						print(f'fault serializer errors: {serializer.errors}')
						print(f'fault serializer error message: {serializer.error_messages}')
						return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
				# Send notification outside the loop
				print('start send_notification ##########')
				await sync_to_async(send_notification)(message=f'fault created-{region.name}')
				print('end send_notification ##########')
				return Response({'message': 'All faults created successfully'}, status=status.HTTP_201_CREATED)

			except Exception as e:
				print(f'error for fault: {e}')
				return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

		return async_to_sync(postData)()

	return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PATCH'])
def custodianPendingFaults(request, pk=None, type=None):
	print('##################### custodianPendingFaults ###########################')
	print(f'pk: {pk}')
	if request.method == 'PATCH':
		print('patch payload:', request.data)
		print('request fault id:', request.data['faultID'])
		async def patchData():
			print('in async fxn')
			# engineer uses this to verify faults
			# print('request fault id type:', type(request.data['faultID']))
			fault = await sync_to_async(Fault.objects.select_related('logged_by__branch__region').get)(pk=request.data['faultID'])
			print(f'verified: {fault.verify_resolve}')
			print(f'verified id: {fault.id}')
			print(f'verified title: {await sync_to_async(lambda: fault.title)()}')
			print(f'verified other: {fault.other}')
			print(f'fault object: {fault}')
			region = fault.logged_by.branch.region
			print(f'region: {region.name}')
			patchSerializer = await sync_to_async(lambda: FaultPatchSerializer(instance=fault, data=request.data, partial=True))()
			print(f'is patchSerializer valid: {await sync_to_async(patchSerializer.is_valid)()}')
			if await sync_to_async(patchSerializer.is_valid)():
				await sync_to_async(patchSerializer.save)()
				print('patch successful ##########')
				print('start send_notification ##########')
				await sync_to_async(send_notification)(message=f'verify resolve-{region.name}')
				print('end send_notification ##########')
				return Response(patchSerializer.data, status=status.HTTP_200_OK)
			else:
				return Response(patchSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
		return async_to_sync(patchData)()
	elif request.method == 'GET':
		async def getData():
			print('##################### custodianPendingFaults (get request) ###########################')
			faultLoggedBy = await sync_to_async(User.objects.get)(pk=pk)
			print(f'faultLoggedBy: {faultLoggedBy}')
			logged_by = await sync_to_async(Custodian.objects.get)(custodian=faultLoggedBy)
			faults = await sync_to_async(lambda: Fault.objects.filter(
				logged_by=logged_by,
				verify_resolve=False,
				confirm_resolve=False,
			).prefetch_related('partfault', 'componentfault'))()
			# print(f'faults: {faults}')
			print()
			faultSerializer = await sync_to_async(lambda: FaultReadSerializer(
					instance=faults,
					many=True
				).data)()
			for (item, faultRequests) in zip(faultSerializer, faults):
				# print('############ item #####################')
				# print(f'faultID: {faultRequests.id}')
				partRequestExist = await sync_to_async(faultRequests.partfault.exists)()
				componentRequestExist = await sync_to_async(faultRequests.componentfault.exists)()
				if any([partRequestExist, componentRequestExist]):
					faultCompRequest = await sync_to_async(lambda: list(faultRequests.componentfault.all()))()
					faultPartRequest = await sync_to_async(lambda: list(faultRequests.partfault.all()))()
					faultCompRequestSerializer = await sync_to_async(lambda: RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True).data)()
					faultPartRequestSerializer = await sync_to_async(lambda: RequestFaultPartReadSerializer(instance=faultPartRequest, many=True).data)()
					item['requestComponent'] = faultCompRequestSerializer if faultCompRequestSerializer else False
					item['requestPart'] = faultPartRequestSerializer if faultPartRequestSerializer else False
				item['requestStatus'] = True if any([partRequestExist, componentRequestExist]) else False
			return faultSerializer
		faultSerializer = async_to_sync(getData)()
		if type == 'list':
			print(f'length of faultSerializer: {len(faultSerializer)}')
			return Response(faultSerializer, status=status.HTTP_200_OK)
		elif type == 'notification':
			faultSerializer = faultSerializer[:5]
			print(f'length of faultSerializer: {len(faultSerializer)}')
			return Response(faultSerializer, status=status.HTTP_200_OK)
		userPaginator = PageNumberPagination()
		userPaginator.page_size = 10  # Number of items per page
		paginated_fault = userPaginator.paginate_queryset(faultSerializer, request)
		print('##################### end engineerUnconfirmedFaults ###########################')
		return userPaginator.get_paginated_response(paginated_fault)

@api_view(['GET',])
def totalCustodianPendingFaults(request, pk=None):
	async def getData():
		print('##################### total custodianPendingFaults ###########################')
		faultLoggedBy = await sync_to_async(User.objects.get)(pk=pk)
		# faultLoggedBy = await sync_to_async(lambda: User.objects.get(pk=pk))()
		custodian = await sync_to_async(Custodian.objects.get)(custodian=faultLoggedBy)
		faults = await sync_to_async(lambda: list(Fault.objects.filter(
			logged_by=custodian,
			verify_resolve=False,
			confirm_resolve=False,
		)))()
		print(f'faults: {len(faults)}')
		print('##################### end total custodianPendingFaults ###########################')
		return Response({'total': len(faults)}, status=status.HTTP_200_OK)
	return async_to_sync(getData)()

# handle engineer, helpdesk, supervisor, etc deliveries counter here.
@api_view(['GET', 'PATCH'])
def custodianUnconfirmedResolutions(request, pk=None, type=None):
	if request.method == 'PATCH':
		async def patchDataFxn():
			print('##################### custodianUnconfirmedResolutions ###########################')
			patchData = {}
			print(f'PATCH payload: {request.data}')
			faultID = request.data['faultID']
			faultLoggedBy = await sync_to_async(User.objects.prefetch_related('custodiandata').get)(pk=pk)
			print(f'faultLoggedBy: {faultLoggedBy}')
			print(f'faultLoggedBy first_name: {faultLoggedBy.first_name}')
			print(f'faultLoggedBy email: {faultLoggedBy.email}')
			region = request.data['region']
			print(f'region: {region}')
			# print(f'custodiandata: {faultLoggedBy.email}')
			custodian = await sync_to_async(Custodian.objects.get)(custodian=faultLoggedBy)
			# print(f'custodian: {await sync_to_async(custodian.custodian.first_name)()}')
			fault = await sync_to_async(lambda: Fault.objects.filter(logged_by=custodian, pk=faultID).first())()
			print(f'fault: {fault}')
			# return Response({'msg': 'good'})
			# print(f'instance: {FaultReadSerializer(fault).data}')
			patchData['confirmed_by'] = pk
			patchData['confirm_resolve'] = request.data['confirm_resolve'] == 'true'
			print(f'patchData: {patchData}')
			confirmResolution = await sync_to_async(lambda: FaultConfirmResolutionSerializer(instance=fault, data=patchData, partial=True))()
			print(f'confirmResolution is valid: {await sync_to_async(confirmResolution.is_valid)()}')
			if await sync_to_async(confirmResolution.is_valid)():
				print(f'confirmResolution passed is valid: {confirmResolution.validated_data}')
				# print(f'Error passed is valid: {confirmResolution.errors}')
				####################################
				await sync_to_async(confirmResolution.save)()
				####################################
				print(f'Confirmaion saved')
				print('start send_notification ##########')
				await sync_to_async(send_notification)(message=f'confirm resolve-{region}')
				print('end send_notification ##########')
				payloadKeys = ['resolvedBy', 'managedBy', 'supervisedBy']
				usersToGetPoints = []
				# allGood = []
				print(f'check deliveries: {request.data["deliveries"]}')
				for index, key in enumerate(payloadKeys):
					print(f'Checking: {key}')
					user = await sync_to_async(User.objects.get)(email=request.data[key])
					print(f'user: {user.first_name}')
					userDelieries = await sync_to_async(Deliveries.objects.select_related('user').get)(user=user)
					print(f'got user delivery mail: {userDelieries.user.first_name}')
					print(f'user email: {request.data[key]}')
					serializeredUserDeliveries = await sync_to_async(lambda: UserDeliveriesSerializer(
						instance=userDelieries,
						data={'deliveries': request.data['deliveries']},
						partial=True
					))()
					print(f'check user is valid: {await sync_to_async(serializeredUserDeliveries.is_valid)()}')
					if await sync_to_async(serializeredUserDeliveries.is_valid)():
						# serializeredUser = serializeredUser.data
						# print(f'serialized user: {serializeredUser.validated_data["id"]}')
						usersToGetPoints.append({index: serializeredUserDeliveries})
					else:
						print(f'error: {serializeredUserDeliveries.errors}')
				print(f'usersToGetPoints: {[obj[i].validated_data for i, obj in enumerate(usersToGetPoints)]}')
				#####################################################
				if len(usersToGetPoints) == 3:
					for index, user in enumerate(usersToGetPoints):
						# print(f'user dict: {user}')
						await sync_to_async(user[index].save)()
						print()
				print('start send_notification ##########')
				await sync_to_async(send_notification)(message=f'deliveries point-{region}')
				print('end send_notification ##########')
				return Response(confirmResolution.data, status=status.HTTP_200_OK)
			# print(f'Error saving confirmation resolution: {confirmResolution.errors}')
			print(f'Error saving confirmation resolution: {confirmResolution.errors}')
			print('##################### end confirmation ###########################')
			return Response(confirmResolution.errors, status=status.HTTP_400_BAD_REQUEST)
		return async_to_sync(patchDataFxn)()
	elif request.method == 'GET':
		async def getData():
			print('##################### custodianUnconfirmedResolutions ###########################')
			print(f'pk: {pk}')
			faultLoggedBy = await sync_to_async(User.objects.get)(pk=pk)
			confirmResolution = await sync_to_async(lambda: Fault.objects.filter(
				logged_by=Custodian.objects.get(custodian=faultLoggedBy),
				verify_resolve=True,
				confirm_resolve=False,
			))()
			# print(f'confirmResolution: {confirmResolution}')
			print()
			faultSerializer = await sync_to_async(lambda: FaultReadSerializer(
					instance=confirmResolution,
					many=True
				).data)()
			# requestStatus = []
			for (item, faultRequests) in zip(faultSerializer, confirmResolution):
				# print('############ item #####################')
				# print(f'faultID: {faultRequests.id}')
				partRequestExist = await sync_to_async(faultRequests.partfault.exists)()
				componentRequestExist = await sync_to_async(faultRequests.componentfault.exists)()
				if any([partRequestExist, componentRequestExist]):
					faultCompRequest = await sync_to_async(lambda: faultRequests.componentfault.all())()
					faultPartRequest = await sync_to_async(lambda: faultRequests.partfault.all())()
					faultCompRequestSerializer = await sync_to_async(lambda: RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True).data)()
					faultPartRequestSerializer = await sync_to_async(lambda: RequestFaultPartReadSerializer(instance=faultPartRequest, many=True).data)()
					item['requestComponent'] = faultCompRequestSerializer if faultCompRequestSerializer else False
					item['requestPart'] = faultPartRequestSerializer if faultPartRequestSerializer else False
				item['requestStatus'] = True if any([partRequestExist, componentRequestExist]) else False
			return faultSerializer
		faultSerializer = async_to_sync(getData)()

		if type == 'list':
			print(f'length of faultSerializer: {len(faultSerializer)}')
			return Response(faultSerializer, status=status.HTTP_200_OK)
		elif type == 'notification':
			faultSerializer = faultSerializer[:5]
			print(f'length of faultSerializer: {len(faultSerializer)}')
			return Response(faultSerializer, status=status.HTTP_200_OK)
		userPaginator = PageNumberPagination()
		userPaginator.page_size = 10  # Number of items per page
		paginated_fault = userPaginator.paginate_queryset(faultSerializer, request)
		print('##################### end ###########################')
		return userPaginator.get_paginated_response(paginated_fault)

@api_view(['GET',])
def totalCustodianUnconfirmedResolutions(request, pk=None):
	async def getData():
		print('##################### total totalCustodianUnconfirmedResolutions ###########################')
		faultLoggedBy = await sync_to_async(User.objects.get)(pk=pk)
		confirmResolution = await sync_to_async(lambda: list(Fault.objects.filter(
			logged_by=Custodian.objects.get(custodian=faultLoggedBy),
			verify_resolve=True,
			confirm_resolve=False,
		)))()
		print(f'faults: {len(confirmResolution)}')
		print('##################### end totalCustodianUnconfirmedResolutions ###########################')
		return Response({'total': len(confirmResolution)}, status=status.HTTP_200_OK)
	return async_to_sync(getData)()

@api_view(['DELETE',])
def deleteFault(request, pk=None):
	async def deleteData():
		print('##################### delete faults ###########################')
		print(f'delete payload: {request.data}')
		print(f'deleting ... ❌❌❌')
		try:
			fault = await sync_to_async(Fault.objects.get)(pk=pk)
		except:
			return Response({'error': 'fault not found'}, status=status.HTTP_404_NOT_FOUND)
		print(f'faultID: {fault.id}')
		await sync_to_async(fault.delete)()
		print(f'done ✅✅✅')
		region = await sync_to_async(lambda: fault.logged_by.branch.region.name)()
		print(f'region: {region}')
		print('start send_notification ##########')
		# print(f'fault deleted-{fault.logged_by.branch.region.name}')
		await sync_to_async(send_notification)(message=f'fault deleted-{region}')
		print('end send_notification ##########')
		print('##################### end delete faults ###########################')
		return Response({'msg': 'deleted successfully'}, status=status.HTTP_200_OK)
	return async_to_sync(deleteData)()

@api_view(['GET'])
def engineerPendingFaults(request, pk=None, type=None):
	print(f'pk: {pk}')
	async def get_data():
		engineer = await sync_to_async(User.objects.get)(pk=pk)
		faults_queryset = Fault.objects.prefetch_related('partfault', 'componentfault')
		faults = await sync_to_async(faults_queryset.filter)(
			assigned_to=engineer,
			verify_resolve=False,
			confirm_resolve=False,
		)

		faultSerializer = await sync_to_async(lambda: FaultReadSerializer(faults, many=True).data)()

		for (item, faultRequests) in zip(faultSerializer, faults):
			faultCompRequest = await sync_to_async(lambda: list(faultRequests.componentfault.all()))()
			faultCompRequestSerializer = await sync_to_async(lambda: RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True).data)()

			item['requestComponent'] = faultCompRequestSerializer if faultCompRequestSerializer else False

			faultPartRequest = await sync_to_async(lambda: list(faultRequests.partfault.all()))()
			faultPartRequestSerializer = await sync_to_async(lambda: RequestFaultPartReadSerializer(instance=faultPartRequest, many=True).data)()

			item['requestPart'] = faultPartRequestSerializer if faultPartRequestSerializer else False
			item['requestStatus'] = bool(faultCompRequestSerializer) or bool(faultPartRequestSerializer)
		return faultSerializer

	faultSerializer = async_to_sync(get_data)()

	if type == 'list':
		return Response(faultSerializer, status=200)
	elif type == 'notification':
		return Response(faultSerializer[:5], status=200)

	paginator = PageNumberPagination()
	paginator.page_size = 10
	paginated_fault = paginator.paginate_queryset(faultSerializer, request)

	return paginator.get_paginated_response(paginated_fault)

@api_view(['GET',])
def totalEngineerPendingFaults(request, pk=None):
	async def getData():
		print('##################### totalEngineerPendingFaults ###########################')
		engineer = await sync_to_async(User.objects.get)(pk=pk)
		totalEngineerFaults = await sync_to_async(lambda: list(Fault.objects.filter(
			assigned_to=engineer,
			verify_resolve=False,
			confirm_resolve=False,
		)))()
		print(f'totalEngineerFaults: {len(totalEngineerFaults)}')
		print('##################### end totalEngineerPendingFaults ###########################')
		return Response({'total': len(totalEngineerFaults)}, status=status.HTTP_200_OK)
	return async_to_sync(getData)()

@api_view(['GET'])
def engineerUnconfirmedFaults(request, pk=None, type=None):
	print('############## engineerUnconfirmedFaults ##############')
	async def get_data():
		print(f'pk: {pk}')
		engineer = await sync_to_async(User.objects.get)(pk=pk)
		print(f'engineer: {engineer}')
		UnconfirmedFaults = await sync_to_async(lambda: list(Fault.objects.filter(
			assigned_to=engineer,
			verify_resolve=True,
			confirm_resolve=False,
		).prefetch_related('partfault', 'componentfault')))()
		# print(f'faults: {UnconfirmedFaults}')

		print()
		faultSerializer = await sync_to_async(lambda: FaultReadSerializer(
				instance=UnconfirmedFaults,
				many=True
			).data)()
		# requestStatus = []
		for (item, faultRequests) in zip(faultSerializer, UnconfirmedFaults):
			# print('############ item #####################')
			print(f'faultID: {faultRequests.id}')
			partRequestExist = await sync_to_async(faultRequests.partfault.exists)()
			componentRequestExist = await sync_to_async(faultRequests.componentfault.exists)()
			print(f'exist: {any([partRequestExist, componentRequestExist])}')
			if any([partRequestExist, componentRequestExist]):
				faultCompRequest = await sync_to_async(lambda: (faultRequests.componentfault.all()))()
				faultPartRequest = await sync_to_async(lambda: (faultRequests.partfault.all()))()
				faultCompRequestSerializer = await sync_to_async(lambda: RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True).data)()
				faultPartRequestSerializer = await sync_to_async(lambda: RequestFaultPartReadSerializer(instance=faultPartRequest, many=True).data)()
				item['requestComponent'] = faultCompRequestSerializer if faultCompRequestSerializer else False
				item['requestPart'] = faultPartRequestSerializer if faultPartRequestSerializer else False
			item['requestStatus'] = True if any([partRequestExist, componentRequestExist]) else False
		return faultSerializer
	faultSerializer = async_to_sync(get_data)()
	if type == 'list':
		print(f'length of faultSerializer: {len(faultSerializer)}')
		return Response(faultSerializer, status=status.HTTP_200_OK)
	elif type == 'notification':
		faultSerializer = faultSerializer[:5]
		print(f'length of faultSerializer: {len(faultSerializer)}')
		return Response(faultSerializer, status=status.HTTP_200_OK)
	userPaginator = PageNumberPagination()
	userPaginator.page_size = 10  # Number of items per page
	paginated_fault = userPaginator.paginate_queryset(faultSerializer, request)
	print('##################### end engineerUnconfirmedFaults ###########################')
	return userPaginator.get_paginated_response(paginated_fault)

@api_view(['GET',])
def totalEngineerUnconfirmedFaults(request, pk=None):
	print('##################### totalEngineerUnconfirmedFaults ###########################')
	async def getData():
		engineer = await sync_to_async(User.objects.get)(pk=pk)
		totalEngineerUnconfirmedFaults = await sync_to_async(lambda: list(Fault.objects.filter(
			assigned_to=engineer,
			verify_resolve=True,
			confirm_resolve=False,
		)))()
		print(f'totalEngineerUnconfirmedFaults: {len(totalEngineerUnconfirmedFaults)}')
		print('##################### end totalEngineerUnconfirmedFaults ###########################')
		return Response({'total': len(totalEngineerUnconfirmedFaults)}, status=status.HTTP_200_OK)
	return async_to_sync(getData)()

###############################################################
@api_view(['GET'])
def regionFaults(request, pk=None, type=None):
	async def getData():
		print('############## help-desk/supervisor Faults ##############')
		user = await sync_to_async(User.objects.get)(pk=pk)

		print(f'user: {user}')
		faults = await sync_to_async(lambda: list(Fault.objects.filter(
			Q(managed_by=user) | Q(supervised_by=user),
			## region=region,
			confirm_resolve=False,
		).prefetch_related('partfault', 'componentfault')))()
		print(f'fault ids: {[fault.id for fault in faults]}')
		print(f'total faults: {len(faults)}')
		# for fault in faults:
		print()

		faultSerializer = await sync_to_async(lambda: FaultReadSerializer(
				instance=faults,
				many=True
			).data)()
		for (item, faultRequests) in zip(faultSerializer, faults):

			partRequestExist = await sync_to_async(faultRequests.partfault.exists)()
			componentRequestExist = await sync_to_async(faultRequests.componentfault.exists)()
			if partRequestExist or componentRequestExist:
				# item['custodianFirstName'] = engineer.first_name
				faultCompRequest = await sync_to_async(lambda: list(faultRequests.componentfault.all()))()
				faultPartRequest = await sync_to_async(lambda: list(faultRequests.partfault.all()))()

				faultCompRequestSerializer = await sync_to_async(lambda: RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True).data)()
				for component in faultCompRequestSerializer:
					component['type'] = 'component'
				faultPartRequestSerializer = await sync_to_async(lambda: RequestFaultPartReadSerializer(instance=faultPartRequest, many=True).data)()
				for part in faultPartRequestSerializer:
					part['type'] = 'part'

				item['requestComponent'] = faultCompRequestSerializer if faultCompRequestSerializer else False
				item['requestPart'] = faultPartRequestSerializer if faultPartRequestSerializer else False
			item['requestStatus'] = bool(partRequestExist) or bool(componentRequestExist)
		return faultSerializer
	faultSerializer = async_to_sync(getData)()
	if type == 'list':
		print(f'length of faultSerializer: {len(faultSerializer)}')
		return Response(faultSerializer, status=status.HTTP_200_OK)
	elif type == 'notification':
		faultSerializer = faultSerializer[:5]
		print(f'length of faultSerializer: {len(faultSerializer)}')
		return Response(faultSerializer, status=status.HTTP_200_OK)
	userPaginator = PageNumberPagination()
	userPaginator.page_size = 10  # Number of items per page
	paginated_fault = userPaginator.paginate_queryset(faultSerializer, request)
	print('##################### end engineerUnconfirmedFaults ###########################')
	return userPaginator.get_paginated_response(paginated_fault)

@api_view(['GET',])
def totalRegionFaults(request, pk=None):
	async def getData():
		print('##################### total help-desk/supervisor Faults ###########################')
		user = await sync_to_async(User.objects.get)(pk=pk)
		totalFaults = await sync_to_async(lambda: list(Fault.objects.filter(
			# managed_by=user,
			Q(managed_by=user) | Q(supervised_by=user),
			verify_resolve=False,
			confirm_resolve=False,
		)))()
		print(f'totalFaults: {len(totalFaults)}')
		print('##################### end total help-desk/supervisor Faults ###########################')
		return Response({'total': len(totalFaults)}, status=status.HTTP_200_OK)
	return async_to_sync(getData)()

####################################################################
@api_view(['GET',])
def engineerUnresolvedFaults(request, pk=None, type=None):
	async def getData():
		print('##################### engineerUnresolvedFaults ###########################')
		print(f'pk: {pk}')
		engineer = await sync_to_async(User.objects.get)(pk=pk)
		print(f'engineer: {engineer}')
		faults = await sync_to_async(lambda: list(Fault.objects.prefetch_related('partfault', 'componentfault').filter(
			assigned_to=engineer,
			confirm_resolve=False,
		)))()
		faultSerializer = await sync_to_async(lambda: FaultReadSerializer(faults, many=True).data)()
		for (item, faultRequests) in zip(faultSerializer, faults):
			faultCompRequest = await sync_to_async(lambda: faultRequests.componentfault.all())()
			faultCompRequestSerializer = await sync_to_async(lambda: RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True).data)()
			for component in faultCompRequestSerializer:
				component['type'] = 'component'
			# if faultCompRequestSerializer.data: print(f'faultCompRequestSerializer: {faultCompRequestSerializer.data}')
			# item['requestStatus'] = True if faultCompRequestSerializer.data else False
			item['requestComponent'] = faultCompRequestSerializer if faultCompRequestSerializer else False
			# print('\n')
			faultPartRequest = await sync_to_async(lambda: faultRequests.partfault.all())()
			faultPartRequestSerializer = await sync_to_async(lambda: RequestFaultPartReadSerializer(instance=faultPartRequest, many=True).data)()
			for part in faultPartRequestSerializer:
				part['type'] = 'part'
			# if faultPartRequestSerializer.data: print(f'faultPartRequestSerializer: {faultPartRequestSerializer.data}')
			item['requestPart'] = faultPartRequestSerializer if faultPartRequestSerializer else False
			item['requestStatus'] = bool(faultCompRequestSerializer) or bool(faultPartRequestSerializer)
			# print(f'#####******########****** requestStatus')
		return faultSerializer
	faultSerializer = async_to_sync(getData)()
	if type == 'list':
		print(f'length of faultSerializer: {len(faultSerializer)}')
		return Response(faultSerializer, status=status.HTTP_200_OK)
	elif type == 'notification':
		faultSerializer = faultSerializer[:5]
		print(f'length of faultSerializer: {len(faultSerializer)}')
		return Response(faultSerializer, status=status.HTTP_200_OK)
	userPaginator = PageNumberPagination()
	userPaginator.page_size = 10  # Number of items per page
	paginated_fault = userPaginator.paginate_queryset(faultSerializer, request)
	print('##################### end engineerUnresolvedFaults ###########################')
	return userPaginator.get_paginated_response(paginated_fault)
	# print('##################### end engineerUnresolvedFaults ###########################')
	# # return userPaginator.get_paginated_response(serialized_data)
	# return Response(faultSerializer, status=status.HTTP_200_OK)

####################################################################
@api_view(['GET',])
def custodianUnresolvedFaults(request, pk=None, type=None):
	async def getData():
		print('##################### custodianUnresolvedFaults ###########################')
		print(f'pk: {pk}')
		custodian = await sync_to_async(User.objects.get)(pk=pk)
		print(f'custodian: {custodian}')
		faults = await sync_to_async(lambda: list(Fault.objects.filter(
			logged_by=Custodian.objects.get(custodian=custodian),
			confirm_resolve=False,
		).prefetch_related('partfault', 'componentfault')))()
		faultSerializer = await sync_to_async(lambda: FaultReadSerializer(
				instance=faults,
				many=True
			).data)()
		# requestStatus = []
		for (item, faultRequests) in zip(faultSerializer, faults):
			# print('############ item #####################')
			# print(f'faultID: {faultRequests.id}')
			partRequestExist = await sync_to_async(faultRequests.partfault.exists)()
			componentRequestExist = await sync_to_async(faultRequests.componentfault.exists)()
			if any([partRequestExist, componentRequestExist]):
				faultCompRequest = await sync_to_async(lambda: list(faultRequests.componentfault.all()))()
				faultPartRequest = await sync_to_async(lambda: list(faultRequests.partfault.all()))()
				faultCompRequestSerializer = await sync_to_async(lambda: RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True).data)()
				for component in faultCompRequestSerializer:
					component['type'] = 'component'
				faultPartRequestSerializer = await sync_to_async(lambda: RequestFaultPartReadSerializer(instance=faultPartRequest, many=True).data)()
				for part in faultPartRequestSerializer:
					part['type'] = 'part'
				item['requestComponent'] = faultCompRequestSerializer if faultCompRequestSerializer else False
				item['requestPart'] = faultPartRequestSerializer if (faultPartRequestSerializer) else False
			item['requestStatus'] = True if any([partRequestExist, componentRequestExist]) else False
		return faultSerializer
	faultSerializer = async_to_sync(getData)()
	if type == 'list':
		print(f'length of faultSerializer: {len(faultSerializer)}')
		return Response(faultSerializer, status=status.HTTP_200_OK)
	elif type == 'notification':
		faultSerializer = faultSerializer[:5]
		print(f'length of faultSerializer: {len(faultSerializer)}')
		return Response(faultSerializer, status=status.HTTP_200_OK)
	userPaginator = PageNumberPagination()
	userPaginator.page_size = 10  # Number of items per page
	paginated_fault = userPaginator.paginate_queryset(faultSerializer, request)
	print('##################### end custodianUnresolvedFaults ###########################')
	return userPaginator.get_paginated_response(paginated_fault)
	# return Response(faultSerializer, status=status.HTTP_200_OK)

###################################################################
################# hr #####################
@api_view(['GET'])
def allFaultsWRequests(request, pk=None, type=None):
	async def getData():
		print('############## human-resource Faults ##############')
		user = await sync_to_async(User.objects.get)(pk=pk)

		print(f'user: {user}')
		# filters for faults with requests that are yet to be atended to
		faults = await sync_to_async(lambda: list(Fault.objects.filter(
			Q(partfault__isnull=False) | Q(componentfault__isnull=False),
			Q(partfault__approved=False, partfault__rejected=False) |
			Q(componentfault__approved=False, componentfault__rejected=False),
			confirm_resolve=False,
			verify_resolve=False
		).distinct().prefetch_related('partfault', 'componentfault')))()

		print(f'fault ids: {[fault.id for fault in faults]}')
		print(f'total faults: {len(faults)}')
		# return Response({'allgood'})
		# for fault in faults:
		print()

		faultSerializer = await sync_to_async(lambda: FaultReadSerializer(
				instance=faults,
				many=True
			).data)()
		for (item, faultRequests) in zip(faultSerializer, faults):
			partRequestExist = await sync_to_async(faultRequests.partfault.exists)()
			componentRequestExist = await sync_to_async(faultRequests.componentfault.exists)()
			# if partRequestExist or componentRequestExist:
				# item['custodianFirstName'] = engineer.first_name
			faultCompRequest = await sync_to_async(lambda: list(faultRequests.componentfault.all()))()
			faultPartRequest = await sync_to_async(lambda: list(faultRequests.partfault.all()))()

			faultCompRequestSerializer = await sync_to_async(lambda: RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True).data)()
			for component in faultCompRequestSerializer:
				component['type'] = 'component'
			faultPartRequestSerializer = await sync_to_async(lambda: RequestFaultPartReadSerializer(instance=faultPartRequest, many=True).data)()
			for part in faultPartRequestSerializer:
				part['type'] = 'part'

			item['requestComponent'] = faultCompRequestSerializer if faultCompRequestSerializer else False
			item['requestPart'] = faultPartRequestSerializer if faultPartRequestSerializer else False
			item['requestStatus'] = bool(partRequestExist) or bool(componentRequestExist)
		return faultSerializer
	faultSerializer = async_to_sync(getData)()
	if type == 'list':
		print(f'length of faultSerializer: {len(faultSerializer)}')
		return Response(faultSerializer, status=status.HTTP_200_OK)
	elif type == 'notification':
		faultSerializer = faultSerializer[:5]
		print(f'length of faultSerializer: {len(faultSerializer)}')
		return Response(faultSerializer, status=status.HTTP_200_OK)
	userPaginator = PageNumberPagination()
	userPaginator.page_size = 10  # Number of items per page
	paginated_fault = userPaginator.paginate_queryset(faultSerializer, request)
	print('##################### end human-resource ###########################')
	return userPaginator.get_paginated_response(paginated_fault)

@api_view(['GET',])
def totalAllFaultsWRequests(request, pk=None):
	async def getData():
		print('##################### total human-resource Faults ###########################')
		user = await sync_to_async(User.objects.get)(pk=pk)
		totalFaults = await sync_to_async(lambda: list(Fault.objects.filter(
			Q(partfault__isnull=False) | Q(componentfault__isnull=False),
			Q(partfault__approved=False, partfault__rejected=False) |
			Q(componentfault__approved=False, componentfault__rejected=False),
			confirm_resolve=False,
			verify_resolve=False
		).distinct().prefetch_related('partfault', 'componentfault')))()
		totalFaults = len(totalFaults)
		print(f'totalFaults: {totalFaults}')
		print('##################### end total human-resource Faults ###########################')
		return Response({'total': totalFaults}, status=status.HTTP_200_OK)
	return async_to_sync(getData)()
