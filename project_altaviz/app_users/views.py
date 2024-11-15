from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from app_bank.models import *
from app_bank.serializers import *
from app_custodian.models import Custodian
from app_custodian.serializers import CustodianCreateUpdateSerializer, CustodianGetUpdateCreateSerializer
from .serializers import *
from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()
from django.core.files import File
from rest_framework.pagination import PageNumberPagination
import os
from django.conf import settings
from app_sse_notification.views import send_sse_notification

def updateDetailesFxn(requestData, user):
	############################ after admin approval ############################
	print(f'\nin the requestData fxn xoxoxoxoxoxo')
	# # print(f'requestData: {requestData}')
	# return 'from requestData fxn xoxoxoxoxoxo\n'
	region = requestData['region']
	state = requestData['state']
	bank = requestData['bank']
	location = requestData['location']
	branch = requestData['branch']
	custodian = user.email
	print(f'region: {region}')
	print(f'state: {state}')
	print(f'bank: {bank}')
	print(f'location: {location}')
	print(f'branch: {branch}')
	print(f'custodian: {custodian}')
	detailsUpdateObject = UpdateLocationAndBranchNotification.objects.create(
		newRegion=requestData['region'],
		newState=requestData['state'],
		newBank=requestData['bank'],
		newLocation=requestData['location'],
		newBranch=requestData['branch'],
		newCustodian=custodian,
		requestUser=user,
	)
	return 'from requestData fxn xoxoxoxoxoxo\n'
	# return Response(serializedUser.data, status=status.HTTP_201_CREATED)

def getOrCreateBankLocationBranch(strObj: dict=None, user: object=None):
	## region
	## region = Region.objects.get(name=strObj['regionStr'])
	# print(f'region: {region}')

	# state
	state = State.objects.get(name=strObj['stateStr'])
	print(f'state: {state}')
	region = state.region
	print(f"region (state's): {region}")

	bank, bCreated = Bank.objects.get_or_create(name=strObj['bankStr'])
	if bCreated: bank.states.add(state)
	print(f'bank: {bank}')
	print(f'new bank: {bCreated}')

	location, new = Location.objects.get_or_create(
		location=strObj['locationStr'],
		state=state,
		region=region,
	)
	print(f'location (no new bank): {location}')
	print(f'new location: {new}')
	if new:
		location.bank.add(bank)
		supervisor = User.objects.get(region=region, role='supervisor')
		print(f'Supervisor: {supervisor.email}')
		print(f'Supervisor role: {supervisor.role}')
		print(f'Supervisor id: {supervisor.id}')
		triggerSupervisorNotification = PatchEngineerAssignmentNotificaionSerializer(
			data={'supervisor': supervisor.id, 'location': location.id}
		)
		print(f'triggerSupervisorNotification is valid: {triggerSupervisorNotification.is_valid()}')
		if triggerSupervisorNotification.is_valid():
			triggerSupervisorNotification.save()
			print('Notification sent successfully &&&&&&&&&&&')
		else:
			print(f'triggerSupervisorNotification error: {triggerSupervisorNotification.errors}')
			print('notification unsuccessful &&&&&&&&&&&')
		###################################################################################################
		# trigger a model that sends a notification to the supervisor to assign an enineer to that location
		###################################################################################################
		print(f'location (with new bank): {location}')
	if user:
		branch, _ = Branch.objects.get_or_create(
			name=strObj['branchStr'],
			custodian=user,
			bank=bank,
			state=state,
			location=location,
			region=region
		)
		print(f'branch id: {branch.id}')
		# print(f'multBranch objects: {[branch.id for branch in multBranch]}')
		print(f'branch object: {branch}')
		# print(f'branch: {data["branch"]}')
		print(f'branch name: {branch.name}')
		print(f'branch id: {branch.id}')
		print(f'branch bank: {branch.bank.name}')
		print(f'branch state: {branch.state.name}')
		print(f'branch location: {branch.location.location}')
		return location, branch
	return location

@api_view(['GET', 'POST'])
def users(request, pk=None):
	# this function creates a new account and objects (if neccessary)
	# and notify the supervisor for engineer assignment to new locations
	custodianSerializer = None
	if request.method == 'POST':
		print('USER payload:', request.data)
		# print(f'the pk is:', pk)
		data = request.data.copy()
		# location = Location.objects.get_or_create()
		data['profile_picture'] = None if data['profile_picture'] == 'null' or data['profile_picture'] == 'undefined' else data['profile_picture']
		print(f'profile_picture: {data["profile_picture"]}')
		requestObject = {
			############ using the bank's region in place of request.data region ############
			# 'regionStr': request.data['region'],
			#################################################################################
			'stateStr': request.data['state'],
			'bankStr': data['bank'],
			'locationStr': data['location'],
			'branchStr': request.data['branch'],
		}
		location = getOrCreateBankLocationBranch(
						strObj=requestObject)
		print(f'location: {location}')
		serializedUser = UserCreateSerializer(data=data)
		# serializedRegion = RegionReadSerializer(data=data)
		print(f'is serializedUser valid:', serializedUser.is_valid())
		# print(f'is serializedRegion valid:', serializedRegion.is_valid())
		# if serializedUser.is_valid() and serializedRegion.is_valid():
		if serializedUser.is_valid():
			role = serializedUser.validated_data['role']
			print(f'role:', role)
			user = serializedUser.save()
			print('user saved successfully')
			if role != 'custodian':
				print(f'user id: {user.id}')
				return Response({'msg': 'Account Created'}, status=status.HTTP_201_CREATED)
			else:
				location, branch = getOrCreateBankLocationBranch(
								strObj=requestObject, user=user)
				print(f'location: {location}')
				print(f'branch: {branch}')
				data['custodian'] = request.data['email']
				print(f'data: {data}')
				data['branch'] = branch.id
				# user = serializedUser.save()
				# return Response({'allgood'})
				custodianSerializer = CustodianCreateUpdateSerializer(data=data)
				print(f'custodian serializer is valid:', custodianSerializer.is_valid())
				if custodianSerializer.is_valid():
					# return Response({'allgood'})
					custodianSerializer.save()
					print('custodian saved successfully')
					print(f'custodian user id: {user.id}')
					return Response({'msg': 'Account Created'}, status=status.HTTP_201_CREATED)
					# return Response(UserReadSerializer(user).data, status=status.HTTP_201_CREATED)
				else:
					print(f'custodian error: {custodianSerializer.errors}')
					# print(f'custodian error: {custodianSerializer.error_messages}')
					return Response({'msg': 'Unsuccessful. Could not create Custodian Account'}, status=status.HTTP_400_BAD_REQUEST)
			# return Response(serializedUser.data, status=status.HTTP_201_CREATED)
		print(f'not a custodian but staff with the role of {request.data["role"]} expert')
		print(f'user error: {serializedUser.errors}')
		return Response({'msg': 'Unsuccessful. Could not create Account'}, status=status.HTTP_400_BAD_REQUEST)
		# print(f'region error: {serializedRegion.errors}')
		# return Response(serializedUser.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'GET':
		# profs = None
		# print('usersDetails:', usersDetails)
		if pk:
			# user = User.objects.select_related('custodiandata').get(pk=pk)
			user = User.objects.get(pk=pk)
			print(f'User: {user}')
			print(f'User.region: {user.region}')
			serializedUser = UserReadSerializer(user).data
			# response_data = serializedUser.data  # Serialized user data
			return Response(serializedUser, status=status.HTTP_200_OK)
		else:
			usersDetails = User.objects.all()
			# print('usersDetails:', usersDetails)
			serializedUser = UserReadSerializer(usersDetails, many=True)
			return Response(serializedUser.data, status=status.HTTP_200_OK)

@api_view(['POST', 'PATCH'])
def userDetaileUpdate(request, pk=None):
	# this function takes the update request for processing and notify the administrator
	# and supervisor for engineer assignments to new location accordingly
	# this should be post request
	user = User.objects.get(pk=pk)
	print(f'user: {user}')
	if request.method == 'POST':
		print('POST payload:', request.data)
		print(f'user pk is:', pk)
		# check for existing and unapproved requests
		previousRequest = UpdateLocationAndBranchNotification.objects.filter(
			requestUser=user,
			approve=False, reject=False
			# status=True
		).first()
		####################################################
		####################################################
		requestLocation = request.data["location"]
		userLocation = user.location.location
		print(f'userLocation: {userLocation}')
		print(f'requestLocation: {requestLocation}')
		changeLocation = requestLocation != userLocation
		print(f'changeLocation (user): {changeLocation}')
		custodian = Custodian.objects.select_related('branch').filter(custodian=user)
		changeBranch = None
		updateDetailes = None
		if custodian:
			branchLocation = custodian.branch.location.location
			print(f'branchLocation: {branchLocation}')
			changeLocation = requestLocation != branchLocation
			print(f'changeLocation (custodian): {changeLocation}')
			requestBranch = request.data['branchID']
			custodianBranch = custodian.branch.id
			print(f'requestBranch: {requestBranch}')
			print(f'custodianBranch: {custodianBranch}')
			changeBranch = int(requestBranch) != int(custodianBranch)
			print(f'changeBranch (custodian): {changeBranch}')
		####################################################
		####################################################

		# if previousRequest:
		# 	print(f'previousRequest: {previousRequest.status}')
		# 	return Response({'msg': 'pending update request'}, status=status.HTTP_200_OK)

		# copy the request data to data and set profile_picture value accordongly
		data = {item: request.data[item] for item in request.data if item != 'profile_picture'}
		profilePictureValue = request.data.get('profile_picture')
		if profilePictureValue in ['null', 'undefined']:
			data['profile_picture'] = None
		else:
			data['profile_picture'] = request.FILES.get('profile_picture', None)
		data['username'] = user.username
		data['email'] = user.email
		data['phone'] = user.phone
		data['location'] = user.location.location
		data['state'] = user.state.name
		data['is_active'] = user.is_active
		print(f'state: {user.state.name}')
		print(f'data: {data}')
		serializedUser = UserUpdateSerializer(instance=user, data=data)
		print(f'is user serializer valid: {serializedUser.is_valid()}')
		# text = None
		if serializedUser.is_valid():
			print(f'validated_data: {serializedUser.validated_data}')
			user = serializedUser.save()
			print(f'user saved ############')
			role = user.role
			print(f'role:', role)
		elif serializedUser.errors:
			print(f'user error: {serializedUser.errors}')
			return Response({'msg': 'Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)
		# check is there is a pending update request and redirects to PATCH if true
		if previousRequest:
			print(f'previousRequest (approve): {previousRequest.approve}')
			print(f'previousRequest (reject): {previousRequest.reject}')
			return Response({'msg': 'pending update request'}, status=status.HTTP_200_OK)
		#############################################################
		#############################################################
		#############################################################
		print()
		print(f'user.role: {user.role}')

		if changeLocation or changeBranch:
			print(f'changeLocation $$$$$: {changeLocation}')
			print(f'changeBranch $$$$$: {changeBranch}')
			# handle this change of branch location upon admin approval
			updateDetailes = updateDetailesFxn(requestData=request.data, user=user)

		# previous user location should be used instead
		# of reassigning to the new location, pending when
		# the change is approved by the administrator
		print(f'updateDetailes: {updateDetailes}')
		#############################################################
		#############################################################
		#############################################################

		additionalText = None
		if changeBranch and not changeLocation:
			additionalText = 'Branch'
		elif changeLocation and not changeBranch:
			additionalText = 'Location'
		elif changeBranch and changeLocation:
			additionalText = 'Location and Branch'
		text = f'Success. Change of {additionalText} will take effect soon as Admin approves'
		if not changeBranch and not changeLocation: text = 'Success'
		resp = {'msg': text}
		print(f'{resp}')
		send_sse_notification('account update request')
		return Response(resp, status=status.HTTP_200_OK)

	# write a patch request to hndle user replacing the current request
	elif request.method == 'PATCH':
		print('PATCH payload:', request.data)
		print(f'user pk is:', pk)
		previousRequest = UpdateLocationAndBranchNotification.objects.filter(
			requestUser=user,
			approve=False, reject=False
			# status=True
		).first()
		print(f'previousRequest id:', previousRequest.id)
		previousRequest.newRegion = request.data['region']
		previousRequest.newState = request.data['state']
		previousRequest.newBank = request.data['bank']
		previousRequest.newLocation = request.data['location']
		previousRequest.newBranch = request.data['branch']
		previousRequest.save()
		print('patch successful')
		return Response({'msg': 'Request Update Successful'}, status=status.HTTP_200_OK)
	return Response({'msg': 'error: wrong request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH', 'GET'])
def approvedDetailsChange(request, pk=None, type=None):
	# this function goes ahead to approve ahe update requests and creates any
	# neccessary objects in the process and notify the supervisor for engineer
	# assignment to new locations
	if request.method == 'PATCH':
		print('approvedDetailsChange payload:', request.data)

		# send along with the request object, the id of the user
		# who requested the change using userID
		user = User.objects.get(pk=request.data['userID'])
		print(f'user: {user}')
		# get the request object
		requestObject = UpdateLocationAndBranchNotification.objects.filter(
			requestUser=user,
			approve=False, reject=False
			# status=True
		).first()
		###################################################################
		###################################################################
		## region = Region.objects.get(name=requestObject.newRegion)
		# print(f'region: {region}')

		# state = State.objects.get(name=requestObject.newState)
		# print(f'state: {state}')

		newRequestObject = {
			'regionStr': requestObject.newRegion,
			'stateStr': requestObject.newState,
			'bankStr': requestObject.newBank,
			'locationStr': requestObject.newLocation,
			'branchStr': requestObject.newBranch,
		}
		location, branch = getOrCreateBankLocationBranch(
						strObj=newRequestObject, user=user)
		print(f'location: {location}')
		print(f'branch: {branch}')
		if user.role == 'custodian':
			custodian = Custodian.objects.get(custodian=user)
			print(f'custodian: {custodian}')
			custodianSerializer = CustodianCreateUpdateSerializer(instance=custodian, data={'branch': branch})
			print(f'custodian serializer is valid:', custodianSerializer.is_valid())
			if custodianSerializer.is_valid():
				# return Response({'allgood'})
				custodianSerializer.save()
				print('custodian saved successfully')
				print(f'custodian user id: {user.id}')
		else:
			print(f'user.location (before): {user.location}')
			user.location = location
			user.save()
			print('user saved successfully')
			print(f'user id: {user.id}')
			print(f'user.location (after): {user.location}')

		# nullify the object
		# handle this status to either approve/reject
		###############################
		if request.data['approve']:
			requestObject.approve = True
		elif request.data['reject']:
			requestObject.reject = True
		###############################
		requestObject.user = None
		requestObject.save()
		return Response({'msg': 'Success'}, status=status.HTTP_200_OK)
		###################################################################
		###################################################################
	elif request.method == 'GET':
		requestObject = UpdateLocationAndBranchNotification.objects.filter(
			approve=False, reject=False
		)
		# print(f'requestObject: {requestObject}')
		############################################################
		# create and use a serializer here to send data to frontend!
		serializedRequests = UpdateLocationAndBranchNotificationSerializer(
			instance=requestObject,
            many=True,
		).data
		# print(f'serializedRequests: {serializedRequests}')
		############################################################
		if type == 'list':
			print(f'length of serializedRequests: {len(serializedRequests)}')
			return Response(serializedRequests, status=status.HTTP_200_OK)
		elif type == 'notification':
			serializedRequests = serializedRequests[:5]
			print(f'length of serializedRequests: {len(serializedRequests)}')
			return Response(serializedRequests, status=status.HTTP_200_OK)
		print(f'length of serializedRequests: {len(serializedRequests)}')
		userPaginator = PageNumberPagination()
		userPaginator.page_size = 10  # Number of items per page
		paginated_fault = userPaginator.paginate_queryset(serializedRequests, request)
		# print('##################### end engineerUnconfirmedFaults ###########################')
		return userPaginator.get_paginated_response(paginated_fault)
	return Response({'msg': 'No notifications'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def totalApprovedDetailsChange(request, pk=None):
	requestObject = UpdateLocationAndBranchNotification.objects.filter(
		approve=False, reject=False
	)
	total = len(requestObject)
	print(f'total: {total}')
	return Response({'total': total}, status=status.HTTP_200_OK)

@api_view(['GET'])
def regionEngineers(request, pk=None):
    # this function goes ahead to get a list of engineers in a specific region
    region = Region.objects.get(
        supervisor=User.objects.get(pk=pk)
        )
    print(f'region: {region.name}')
    engineers = User.objects.filter(region=region, role='engineer')
    print(f'engineers: {[f"name: {engineer.first_name} and id: {engineer.id}" for engineer in engineers]}')
    serializedEngineers = UserSummarizedDetailsSerializer(instance=engineers, many=True)
    return Response(serializedEngineers.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PATCH'])
def assignEngineerToLocation(request, pk=None, type=None):
	# this function goes ahead to assign an engineer to a new location
	print('assignEngineerToLocation pk:', pk)
	if request.method == 'PATCH':
		supervisor = User.objects.get(pk=pk)
		print(f'supevisor:', supervisor)
		print('assignEngineerToLocation PATCH payload:', request.data)
		listKeys = list(request.data)
		print(f'list version: {listKeys}')
		for key in listKeys:
			locationName, locationID = key.split('-')
			engineerName, engineerEmail, engineerID = request.data[key].split(')-(')
			print(f'locationName: {locationName}')
			print(f'locationID: {locationID}')
			print(f'engineerName: {engineerName}')
			print(f'engineerEmail: {engineerEmail}')
			print(f'engineerID: {engineerID}')
			newLocation = Location.objects.get(pk=locationID)
			print(f'newLocation: {newLocation}')
			engineer = User.objects.get(pk=engineerID)
			print(f'engineer: {engineer}')
			branch = Branch.objects.filter(location=newLocation)
			print(f'check branch: {branch}')
			print(f'check engineer: {Engineer.objects.filter(location=newLocation)}')
			assignedEngineer = Engineer.objects.create(
				engineer=engineer,
                location=newLocation,
			)
			print(f'assignedEngineer obj: {assignedEngineer}')
			if branch:
				branch = branch[0]
				print(f'branch engineer (before): {branch.branch_engineer}')
				branch.branch_engineer = assignedEngineer
				branch.save()
				print(f'branch engineer (after): {branch.branch_engineer}')
				notificationStatus = EngineerAssignmentNotificaion.objects.get(
					location=newLocation
				)
				print(f'notification status: {notificationStatus}')
				print(f'notification status: {notificationStatus.status}')
				notificationStatus.status = False
				notificationStatus.save()
				print(f'notification status: {notificationStatus.status}')
			print('#######################')
			print()
		send_sse_notification('assigned engineer to new location')
		return Response({'msg': 'Success'}, status=status.HTTP_200_OK)
	elif request.method == 'GET':
		supervisor = User.objects.get(pk=pk)
		notifications = EngineerAssignmentNotificaion.objects.filter(
			supervisor=supervisor, status=True
		)
		if notifications:
			serializedNotifications = EngineerAssignmentNotificaionSerializer(
				instance=notifications, many=True
			).data
			print(f'notifications: {[notification.id for notification in notifications]}')
			# return Response(serializedNotifications, status=status.HTTP_200_OK)
			if type == 'list':
				print(f'length of serializedNotifications: {len(serializedNotifications)}')
				return Response(serializedNotifications, status=status.HTTP_200_OK)
			elif type == 'notification':
				serializedNotifications = serializedNotifications[:5]
				print(f'length of serializedNotifications: {len(serializedNotifications)}')
				return Response(serializedNotifications, status=status.HTTP_200_OK)
			userPaginator = PageNumberPagination()
			userPaginator.page_size = 10  # Number of items per page
			paginated_fault = userPaginator.paginate_queryset(serializedNotifications, request)
			# print('##################### end engineerUnconfirmedFaults ###########################')
			return userPaginator.get_paginated_response(paginated_fault)
		return Response({'msg': 'No notifications'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def totalAssignEngineerToLocation(request, pk=None):
	# this function goes ahead to assign an engineer to a new location
	print('totalAssignEngineerToLocation pk:', pk)
	supervisor = User.objects.get(pk=pk)
	notifications = EngineerAssignmentNotificaion.objects.filter(
		supervisor=supervisor, status=True
	)
	if notifications:
		print(f'total length of update request: {len(notifications)}')
		return Response({'total': len(notifications)}, status=status.HTTP_200_OK)
	return Response({'msg': 'No notifications'}, status=status.HTTP_200_OK)
