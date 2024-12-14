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
# from app_sse_notification.views import send_sse_notification
from app_sse_notification.utils import send_websocket_notification

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
	faultNames = FaultName.objects.all()
	print(f'faultNames: {faultNames}')
	serializer = FaultNameSerializer(faultNames, many=True)
	print(f'faultNames serialized: {serializer.data}')
	return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
def faultDetail(request, pk=None):
	faultObj = Fault.objects.get(pk=pk)
	print(f'faultObj: {faultObj}')
	serializer = FaultCreateUpdateSerializer(instance=faultObj)
	print(f'faultObj serialized: {serializer.data}')
	return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def fault(request, pk=None):
	# faultDetails = Fault.objects.all()
	if request.method == 'POST':
		region = Region.objects.get(name=request.data['region'])
		print('fault payload:', request.data)
		location = Location.objects.get(
			location=request.data['location'],
			bank=Bank.objects.get(name=request.data['bank']),
			state=State.objects.get(name=request.data['state']),
			region=region,
		)
		assigned_to = request.data['assigned_to']
		supervised_by = request.data['supervised_by']
		managed_by = request.data['managed_by']
		logged_by = request.data['logged_by']
		# print(f'email: {email}')
		print(f'location id: {location.id}')
		print(f'assigned_to: {assigned_to}')
		print(f'supervised_by: {supervised_by}')
		print(f'managed_by: {managed_by}')
		print(f'logged_by: {logged_by}')
		dictionary = {item: request.data[item] for item in list(request.data)}
		print(f'dictionary: {dictionary}')
		dicttn = {}
		faultList = [i for i in (list(request.data)) if i.startswith('fault') or i.startswith('other')]
		dictOfLists = compartmentalizedList(faultList)
		length = len(dictOfLists)
		print('dictOfLists:', dictOfLists)
		print('list version:', faultList)
		print('length:', length)
		for item in dictOfLists.values():
			print(f'item:', item)
			# dicttn['title'] = FaultName.objects.get(name=request.data[item[0]])
			dicttn['title'] = request.data[item[0]]
			if len(item) > 1:
				dicttn['other'] = request.data[item[1]]
			else:
				dicttn['other'] = None
			dicttn.update({item: request.data[item] for item in list(request.data)})
			dicttn['location'] = location.id
			print(f'new dicttn:', dicttn)
			# return Response({'allgood'})
			serializer = FaultCreateUpdateSerializer(data=dicttn)
			print(f'is serializer valid:', serializer.is_valid())
			if serializer.is_valid():
				length -= 1
				# if length % 2	== 0:
				serializer.save()
				print(f'saved: {dicttn}')
				print(f'SAVED #########################')
				if length != 0:
					continue
				print('start send_websocket_notification ##########')
				send_websocket_notification(f'fault created-{region.name}')
				print('end send_websocket_notification ##########')
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			print(f'serializer.errors: {serializer.errors}')
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
def custodianPendingFaults(request, pk=None, type=None):
	print('##################### custodianPendingFaults ###########################')
	print(f'pk: {pk}')
	if request.method == 'PATCH':
		# engineer uses this to verify faults
		print('patch payload:', request.data)
		# patchData = request.data.copy()
		# patchData['verify_resolve'] = request.data['verify_resolve'] == 'true' if request.data['verify_resolve'] else None
		# print('patchData:', patchData)
		print('request fault id:', request.data['faultID'])
		# print('request fault id type:', type(request.data['faultID']))
		fault = Fault.objects.get(pk=request.data['faultID'])
		print(f'verified: {fault.verify_resolve}')
		print(f'verified id: {fault.id}')
		print(f'verified title: {fault.title}')
		print(f'verified other: {fault.other}')
		print(f'fault object: {fault}')
		region = fault.logged_by.branch.region.name
		print(f'region: {region}')
		patchSerializer = FaultPatchSerializer(instance=fault, data=request.data, partial=True)
		print(f'is patchSerializer valid: {patchSerializer.is_valid()}')
		if patchSerializer.is_valid():
			patchSerializer.save()
			print('patch successful ##########')
			# resolvedFault = Fault.objects.get(pk=request.data['faultID'])
			# print(f'verified: {resolvedFault.verify_resolve}')
			# print(f'verified id: {resolvedFault.id}')
			# print(f'verified title: {resolvedFault.title}')
			# print(f'verified other: {resolvedFault.other}')
			# print(f'fault object: {resolvedFault}')
			print('start send_websocket_notification ##########')
			send_websocket_notification(f'verify resolve-{region}')
			print('end send_websocket_notification ##########')
			return Response(patchSerializer.data, status=status.HTTP_200_OK)
		return Response(patchSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		print('##################### custodianPendingFaults (get request) ###########################')
		faultLoggedBy = User.objects.get(pk=pk)
		print(f'faultLoggedBy: {faultLoggedBy}')
		faults = Fault.objects.filter(
			logged_by=Custodian.objects.get(custodian=faultLoggedBy),
			verify_resolve=False,
			confirm_resolve=False,
		).prefetch_related('partfault', 'componentfault')
		# print(f'faults: {faults}')
		print()
		faultSerializer = FaultReadSerializer(
				instance=faults,
				many=True
			).data
		for (item, faultRequests) in zip(faultSerializer, faults):
			# print('############ item #####################')
			# print(f'faultID: {faultRequests.id}')
			partRequestExist = faultRequests.partfault.exists()
			componentRequestExist = faultRequests.componentfault.exists()
			if any([partRequestExist, componentRequestExist]):
				faultCompRequest = faultRequests.componentfault.all()
				faultPartRequest = faultRequests.partfault.all()
				faultCompRequestSerializer = RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True)
				faultPartRequestSerializer = RequestFaultPartReadSerializer(instance=faultPartRequest, many=True)
				item['requestComponent'] = faultCompRequestSerializer.data if faultCompRequestSerializer.data else False
				item['requestPart'] = faultPartRequestSerializer.data if (faultPartRequestSerializer.data or faultPartRequestSerializer.data) else False
			item['requestStatus'] = True if any([partRequestExist, componentRequestExist]) else False
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
	print('##################### total custodianPendingFaults ###########################')
	faultLoggedBy = User.objects.get(pk=pk)
	faults = Fault.objects.filter(
		logged_by=Custodian.objects.get(custodian=faultLoggedBy),
		verify_resolve=False,
		confirm_resolve=False,
	)
	print(f'faults: {len(faults)}')
	print('##################### end total custodianPendingFaults ###########################')
	return Response({'total': len(faults)}, status=status.HTTP_200_OK)

# handle engineer, helpdesk, supervisor, etc deliveries counter here.
@api_view(['GET', 'PATCH'])
def custodianUnconfirmedResolutions(request, pk=None, type=None):
	if request.method == 'PATCH':
		print('##################### custodianUnconfirmedResolutions ###########################')
		patchData = {}
		print(f'PATCH payload: {request.data}')
		faultID = request.data['faultID']
		faultLoggedBy = User.objects.prefetch_related('custodiandata').get(pk=pk)
		print(f'faultLoggedBy: {faultLoggedBy}')
		print(f'faultLoggedBy first_name: {faultLoggedBy.first_name}')
		print(f'faultLoggedBy email: {faultLoggedBy.email}')
		# print(f'custodiandata: {faultLoggedBy.email}')
		custodian = Custodian.objects.get(custodian=faultLoggedBy)
		print(f'custodian: {custodian}')
		fault = Fault.objects.filter(logged_by=custodian, pk=faultID).first()
		print(f'fault: {fault}')
		# return Response({'msg': 'good'})
		# print(f'instance: {FaultReadSerializer(fault).data}')
		patchData['confirmed_by'] = pk
		patchData['confirm_resolve'] = request.data['confirm_resolve'] == 'true'
		print(f'patchData: {patchData}')
		confirmResolution = FaultConfirmResolutionSerializer(instance=fault, data=patchData, partial=True)
		print(f'confirmResolution is valid: {confirmResolution.is_valid()}')
		if confirmResolution.is_valid():
			print(f'confirmResolution passed is valid: {confirmResolution.validated_data}')
			# print(f'Error passed is valid: {confirmResolution.errors}')
			####################################
			confirmResolution.save()
			####################################
			print(f'Confirmaion saved')
			print('start send_websocket_notification ##########')
			send_websocket_notification(f'confirm resolve-{faultLoggedBy.region.name}')
			print('end send_websocket_notification ##########')
			payloadKeys = ['resolvedBy', 'managedBy', 'supervisedBy']
			usersToGetPoints = []
			# allGood = []
			print(f'check deliveries: {request.data["deliveries"]}')
			for index, key in enumerate(payloadKeys):
				print(f'Checking: {key}')
				user = User.objects.get(email=request.data[key])
				print(f'user: {user.first_name}')
				userDelieries = Deliveries.objects.get(user=user)
				print(f'got user delivery mail: {userDelieries.user.first_name}')
				print(f'user email: {request.data[key]}')
				serializeredUserDeliveries = UserDeliveriesSerializer(
					instance=userDelieries,
					data={'deliveries': request.data['deliveries']},
					partial=True
				)
				print(f'check user is valid: {serializeredUserDeliveries.is_valid()}')
				if serializeredUserDeliveries.is_valid():
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
					user[index].save()
					print()
			print('start send_websocket_notification ##########')
			send_websocket_notification(f'deliveries point-{faultLoggedBy.region.name}')
			print('end send_websocket_notification ##########')
			return Response(confirmResolution.data, status=status.HTTP_200_OK)
		# print(f'Error saving confirmation resolution: {confirmResolution.errors}')
		print(f'Error saving confirmation resolution: {confirmResolution.errors}')
		print('##################### end confirmation ###########################')
		return Response(confirmResolution.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		print('##################### custodianUnconfirmedResolutions ###########################')
		print(f'pk: {pk}')
		faultLoggedBy = User.objects.get(pk=pk)
		confirmResolution = Fault.objects.filter(
			logged_by=Custodian.objects.get(custodian=faultLoggedBy),
			verify_resolve=True,
			confirm_resolve=False,
		)
		# print(f'confirmResolution: {confirmResolution}')
		print()
		faultSerializer = FaultReadSerializer(
				instance=confirmResolution,
				many=True
			).data
		# requestStatus = []
		for (item, faultRequests) in zip(faultSerializer, confirmResolution):
			# print('############ item #####################')
			# print(f'faultID: {faultRequests.id}')
			partRequestExist = faultRequests.partfault.exists()
			componentRequestExist = faultRequests.componentfault.exists()
			if any([partRequestExist, componentRequestExist]):
				faultCompRequest = faultRequests.componentfault.all()
				faultPartRequest = faultRequests.partfault.all()
				# print(f'	faultCompRequest: {[request.id for request in faultCompRequest]}')
				# print(f'	faultPartRequest: {[part.id for part in faultPartRequest]}')
				faultCompRequestSerializer = RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True)
				faultPartRequestSerializer = RequestFaultPartReadSerializer(instance=faultPartRequest, many=True)
				item['requestComponent'] = faultCompRequestSerializer.data if faultCompRequestSerializer.data else False
				item['requestPart'] = faultPartRequestSerializer.data if (faultPartRequestSerializer.data) else False
			item['requestStatus'] = True if any([partRequestExist, componentRequestExist]) else False

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
	print('##################### total totalCustodianUnconfirmedResolutions ###########################')
	faultLoggedBy = User.objects.get(pk=pk)
	confirmResolution = Fault.objects.filter(
		logged_by=Custodian.objects.get(custodian=faultLoggedBy),
		verify_resolve=True,
		confirm_resolve=False,
	)
	print(f'faults: {len(confirmResolution)}')
	print('##################### end totalCustodianUnconfirmedResolutions ###########################')
	return Response({'total': len(confirmResolution)}, status=status.HTTP_200_OK)

@api_view(['DELETE',])
def deleteFault(request, pk=None):
	print('##################### delete faults ###########################')
	try:
		fault = Fault.objects.get(pk=pk)
	except:
		return Response({'error': 'fault not found'}, status=status.HTTP_404_NOT_FOUND)
	print(f'fault: {fault}')
	fault.delete()
	print('##################### end delete faults ###########################')
	return Response({'msg': 'deleted successfully'}, status=status.HTTP_200_OK)

# ########################################
@api_view(['GET',])
def engineerPendingFaults(request, pk=None, type=None):
	print('##################### engineerPendingFaults ###########################')
	print(f'pk: {pk}')
	engineer = User.objects.get(pk=pk)
	print(f'engineer: {engineer}')
	faults = Fault.objects.prefetch_related('partfault', 'componentfault').filter(
		assigned_to=engineer,
		verify_resolve=False,
		confirm_resolve=False,
	)
	faultSerializer = FaultReadSerializer(faults, many=True).data
	print()
	for (item, faultRequests) in zip(faultSerializer, faults):
		faultCompRequest = faultRequests.componentfault.all()
		faultCompRequestSerializer = RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True)
		# if faultCompRequestSerializer.data: print(f'faultCompRequestSerializer: {faultCompRequestSerializer.data}')
		# item['requestStatus'] = True if faultCompRequestSerializer.data else False
		item['requestComponent'] = faultCompRequestSerializer.data if faultCompRequestSerializer.data else False
		# print('\n')
		faultPartRequest = faultRequests.partfault.all()
		faultPartRequestSerializer = RequestFaultPartReadSerializer(instance=faultPartRequest, many=True)
		# if faultPartRequestSerializer.data: print(f'faultPartRequestSerializer: {faultPartRequestSerializer.data}')
		item['requestPart'] = faultPartRequestSerializer.data if (faultPartRequestSerializer.data or faultPartRequestSerializer.data) else False
		item['requestStatus'] = bool(faultCompRequestSerializer.data) or bool(faultPartRequestSerializer.data)
		# print(f'#####******########****** requestStatus: {bool(faultCompRequestSerializer.data) or bool(faultPartRequestSerializer.data)}')
	print('##################### end engineerPendingFaults ###########################')
	# where i am #############################
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
	# return userPaginator.get_paginated_response(serialized_data)

@api_view(['GET',])
def totalEngineerPendingFaults(request, pk=None):
	print('##################### totalEngineerPendingFaults ###########################')
	engineer = User.objects.get(pk=pk)
	totalEngineerFaults = Fault.objects.filter(
		assigned_to=engineer,
		verify_resolve=False,
		confirm_resolve=False,
	).count()
	print(f'totalEngineerFaults: {totalEngineerFaults}')
	print('##################### end totalEngineerPendingFaults ###########################')
	return Response({'total': totalEngineerFaults}, status=status.HTTP_200_OK)

@api_view(['GET'])
def engineerUnconfirmedFaults(request, pk=None, type=None):
	print('############## engineerUnconfirmedFaults ##############')
	print(f'pk: {pk}')
	engineer = User.objects.get(pk=pk)
	print(f'engineer: {engineer}')
	UnconfirmedFaults = Fault.objects.filter(
		assigned_to=engineer,
		verify_resolve=True,
		confirm_resolve=False,
	).prefetch_related('partfault', 'componentfault')
	# print(f'faults: {UnconfirmedFaults}')

	print()
	faultSerializer = FaultReadSerializer(
			instance=UnconfirmedFaults,
			many=True
		).data
	# requestStatus = []
	for (item, faultRequests) in zip(faultSerializer, UnconfirmedFaults):
		# print('############ item #####################')
		# print(f'faultID: {faultRequests.id}')
		partRequestExist = faultRequests.partfault.exists()
		componentRequestExist = faultRequests.componentfault.exists()
		if any([partRequestExist, componentRequestExist]):
			faultCompRequest = faultRequests.componentfault.all()
			faultPartRequest = faultRequests.partfault.all()
			# print(f'	faultCompRequest: {[request.id for request in faultCompRequest]}')
			# print(f'	faultPartRequest: {[part.id for part in faultPartRequest]}')
			faultCompRequestSerializer = RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True)
			faultPartRequestSerializer = RequestFaultPartReadSerializer(instance=faultPartRequest, many=True)
			item['requestComponent'] = faultCompRequestSerializer.data if faultCompRequestSerializer.data else False
			item['requestPart'] = faultPartRequestSerializer.data if (faultPartRequestSerializer.data) else False
		item['requestStatus'] = True if any([partRequestExist, componentRequestExist]) else False
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
	engineer = User.objects.get(pk=pk)
	totalEngineerUnconfirmedFaults = Fault.objects.filter(
		assigned_to=engineer,
		verify_resolve=True,
		confirm_resolve=False,
	)
	print(f'totalEngineerUnconfirmedFaults: {len(totalEngineerUnconfirmedFaults)}')
	print('##################### end totalEngineerUnconfirmedFaults ###########################')
	return Response({'total': len(totalEngineerUnconfirmedFaults)}, status=status.HTTP_200_OK)

###############################################################
@api_view(['GET'])
def regionFaults(request, pk=None, type=None):
	print('############## help-desk/supervisor Faults ##############')
	user = User.objects.get(pk=pk)

	print(f'user: {user}')
	faults = Fault.objects.filter(
		Q(managed_by=user) | Q(supervised_by=user),
		## region=region,
		confirm_resolve=False,
	).prefetch_related('partfault', 'componentfault')
	print(f'fault ids: {[fault.id for fault in faults]}')
	print(f'total faults: {len(faults)}')
	# for fault in faults:
	print()

	faultSerializer = FaultReadSerializer(
			instance=faults,
			many=True
		).data
	for (item, faultRequests) in zip(faultSerializer, faults):

		partRequestExist = faultRequests.partfault.exists()
		componentRequestExist = faultRequests.componentfault.exists()
		if partRequestExist or componentRequestExist:
			# item['custodianFirstName'] = engineer.first_name
			faultCompRequest = faultRequests.componentfault.all()
			faultPartRequest = faultRequests.partfault.all()

			faultCompRequestSerializer = RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True).data
			for component in faultCompRequestSerializer:
				component['type'] = 'component'
			faultPartRequestSerializer = RequestFaultPartReadSerializer(instance=faultPartRequest, many=True).data
			for part in faultPartRequestSerializer:
				part['type'] = 'part'

			item['requestComponent'] = faultCompRequestSerializer if faultCompRequestSerializer else False
			item['requestPart'] = faultPartRequestSerializer if faultPartRequestSerializer else False
		item['requestStatus'] = bool(partRequestExist) or bool(componentRequestExist)
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
	print('##################### total help-desk/supervisor Faults ###########################')
	user = User.objects.get(pk=pk)
	totalFaults = Fault.objects.filter(
		# managed_by=user,
		Q(managed_by=user) | Q(supervised_by=user),
		verify_resolve=False,
		confirm_resolve=False,
	).count()
	print(f'totalFaults: {totalFaults}')
	print('##################### end total help-desk/supervisor Faults ###########################')
	return Response({'total': totalFaults}, status=status.HTTP_200_OK)

####################################################################
@api_view(['GET',])
def engineerUnresolvedFaults(request, pk=None, type=None):
	print('##################### engineerUnresolvedFaults ###########################')
	print(f'pk: {pk}')
	engineer = User.objects.get(pk=pk)
	print(f'engineer: {engineer}')
	faults = Fault.objects.prefetch_related('partfault', 'componentfault').filter(
		assigned_to=engineer,
		confirm_resolve=False,
	)
	faultSerializer = FaultReadSerializer(faults, many=True).data
	for (item, faultRequests) in zip(faultSerializer, faults):
		faultCompRequest = faultRequests.componentfault.all()
		faultCompRequestSerializer = RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True).data
		for component in faultCompRequestSerializer:
			component['type'] = 'component'
		# if faultCompRequestSerializer.data: print(f'faultCompRequestSerializer: {faultCompRequestSerializer.data}')
		# item['requestStatus'] = True if faultCompRequestSerializer.data else False
		item['requestComponent'] = faultCompRequestSerializer if faultCompRequestSerializer else False
		# print('\n')
		faultPartRequest = faultRequests.partfault.all()
		faultPartRequestSerializer = RequestFaultPartReadSerializer(instance=faultPartRequest, many=True).data
		for part in faultPartRequestSerializer:
			part['type'] = 'part'
		# if faultPartRequestSerializer.data: print(f'faultPartRequestSerializer: {faultPartRequestSerializer.data}')
		item['requestPart'] = faultPartRequestSerializer if faultPartRequestSerializer else False
		item['requestStatus'] = bool(faultCompRequestSerializer) or bool(faultPartRequestSerializer)
		# print(f'#####******########****** requestStatus')
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
	print('##################### custodianUnresolvedFaults ###########################')
	print(f'pk: {pk}')
	custodian = User.objects.get(pk=pk)
	print(f'custodian: {custodian}')
	faults = Fault.objects.filter(
		logged_by=Custodian.objects.get(custodian=custodian),
		confirm_resolve=False,
	).prefetch_related('partfault', 'componentfault')
	faultSerializer = FaultReadSerializer(
			instance=faults,
			many=True
		).data
	# requestStatus = []
	for (item, faultRequests) in zip(faultSerializer, faults):
		# print('############ item #####################')
		# print(f'faultID: {faultRequests.id}')
		partRequestExist = faultRequests.partfault.exists()
		componentRequestExist = faultRequests.componentfault.exists()
		if any([partRequestExist, componentRequestExist]):
			faultCompRequest = faultRequests.componentfault.all()
			faultPartRequest = faultRequests.partfault.all()
			# print(f'	faultCompRequest: {[request.id for request in faultCompRequest]}')
			# print(f'	faultPartRequest: {[part.id for part in faultPartRequest]}')
			faultCompRequestSerializer = RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True).data
			for component in faultCompRequestSerializer:
				component['type'] = 'component'
			faultPartRequestSerializer = RequestFaultPartReadSerializer(instance=faultPartRequest, many=True).data
			for part in faultPartRequestSerializer:
				part['type'] = 'part'
			item['requestComponent'] = faultCompRequestSerializer if faultCompRequestSerializer else False
			item['requestPart'] = faultPartRequestSerializer if (faultPartRequestSerializer) else False
		item['requestStatus'] = True if any([partRequestExist, componentRequestExist]) else False
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
	print('############## human-resource Faults ##############')
	user = User.objects.get(pk=pk)

	print(f'user: {user}')
	# filters for faults with requests that are yet to be atended to
	faults = Fault.objects.filter(
		Q(partfault__isnull=False) | Q(componentfault__isnull=False),
		Q(partfault__approved=False, partfault__rejected=False) |
		Q(componentfault__approved=False, componentfault__rejected=False),
		confirm_resolve=False,
		verify_resolve=False
	).distinct().prefetch_related('partfault', 'componentfault')

	print(f'fault ids: {[fault.id for fault in faults]}')
	print(f'total faults: {len(faults)}')
	# return Response({'allgood'})
	# for fault in faults:
	print()

	faultSerializer = FaultReadSerializer(
			instance=faults,
			many=True
		).data
	for (item, faultRequests) in zip(faultSerializer, faults):
		partRequestExist = faultRequests.partfault.exists()
		componentRequestExist = faultRequests.componentfault.exists()
		# if partRequestExist or componentRequestExist:
			# item['custodianFirstName'] = engineer.first_name
		faultCompRequest = faultRequests.componentfault.all()
		faultPartRequest = faultRequests.partfault.all()

		faultCompRequestSerializer = RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True).data
		for component in faultCompRequestSerializer:
			component['type'] = 'component'
		faultPartRequestSerializer = RequestFaultPartReadSerializer(instance=faultPartRequest, many=True).data
		for part in faultPartRequestSerializer:
			part['type'] = 'part'

		item['requestComponent'] = faultCompRequestSerializer if faultCompRequestSerializer else False
		item['requestPart'] = faultPartRequestSerializer if faultPartRequestSerializer else False
		item['requestStatus'] = bool(partRequestExist) or bool(componentRequestExist)
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
	print('##################### total human-resource Faults ###########################')
	user = User.objects.get(pk=pk)
	totalFaults = Fault.objects.filter(
		Q(partfault__isnull=False) | Q(componentfault__isnull=False),
		Q(partfault__approved=False, partfault__rejected=False) |
		Q(componentfault__approved=False, componentfault__rejected=False),
		confirm_resolve=False,
		verify_resolve=False
	).distinct().prefetch_related('partfault', 'componentfault')
	totalFaults = len(totalFaults)
	print(f'totalFaults: {totalFaults}')
	print('##################### end total human-resource Faults ###########################')
	return Response({'total': totalFaults}, status=status.HTTP_200_OK)
