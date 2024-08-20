from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from app_bank.models import *
from app_bank.serializers import *
from .serializers import *
from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()

# Create your views here.

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def users(request, pk=None):
	usersDetails = User.objects.all()
	custodianDetails = Custodian.objects.all()
	# print(f'usersDetails: {usersDetails}')
	custodianSerializer = None
	if request.method == 'POST':
		print('USER payload:', request.data)
		serializer = UserCreateUpdateSerializer(data=request.data)
		
		print(f'is serializer valid:', serializer.is_valid())
		if serializer.is_valid():
			department = serializer.validated_data['department']

			user = serializer.save()
			print(f'user saved and created')
			print(f'department.name', department.name)
			print(f'is department custodian:', department.name == 'custodian')
			if department.name == 'custodian':
				bankName = request.data['bank']
				print(f'bankName: {bankName}')
				bank = Bank.objects.get(name=bankName)
				print(f'bank obj: {bank}')
				custodianSerializer = CustodianSerializer(data=request.data)
				print(f'custodian serializer is valid:', custodianSerializer.is_valid())
				if custodianSerializer.is_valid():
					custodianSerializer.save()
					print('custodian saved successfully')
					return Response(UserReadSerializer(user).data, status=status.HTTP_201_CREATED)
				else:
					print(custodianSerializer.errors)
					return Response(custodianSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

			# return Response(serializer.data, status=status.HTTP_201_CREATED)
			# email = request.data['email']
			# username = request.data['username']
			# department = Department.objects.get(name=request.data['department'])
			# password = request.data['password']
			# print(f'email: {email}, password: {password}')
			# user = User.objects.create_user(email=email, password=password, username=username, department=department)
			# user.save()
			# print('USER created')
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	# elif request.method == 'PUT':
	#     print('USER payload:', request.data)
	#     user = get_object_or_404(User, pk=pk)
	#     print(f'user: {user}')
	#     serializer = UserSerializer(user, data=request.data, partial=True)
	#     print(f'is serializer valid:', serializer.is_valid())
	#     if serializer.is_valid():
	#         serializer.save()
	#         print(f'user updated')
	#         return Response(serializer.data, status=status.HTTP_200_OK)
	#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	# elif request.method == 'DELETE':
	#     user = get_object_or_404(User, pk=pk)
	#     user.delete()
	#     print('USER deleted')
	#     return Response(status=status.HTTP_204_NO_CONTENT)
	elif request.method == 'GET':
		print('usersDetails:', usersDetails)
		if pk:
			user = User.objects.select_related('mail').get(pk=pk)
			try:
				cust = Custodian.objects.select_related('bank').get(email=user)
				print(f'bank: {cust.bank}')
				print(f'custodian: {cust}')
			except:
				pass
			print(f'user: {user}')
			# custodian = get_object_or_404(Custodian, pk=pk)
			print(f'user: {user}')
			serializer = UserReadSerializer(user, context={'request': request})
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			print('usersDetails:', usersDetails)
			serializer = UserReadSerializer(usersDetails, context={'request': request}, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		# serializer = UserSerializer(usersDetails, many=True)
		# return Response(serializer.data)
		# return Response({"home": "welcome home from django server. This information is from the backend server"}, status=status.HTTP_200_OK)
	# else:
	#     print('usersDetails:', usersDetails)
	#     serializer = UserSerializer(usersDetails, many=True)
	#     return Response(serializer.data, status=status.HTTP_200_OK)
	# return Response({"home": "welcome home from django server. This information is from the backend server"}, status=status.HTTP_200_OK)
	# serializer = UserSerializer(usersDetails, many=True)
	# return Response(serializer.data)
	# serializer = UserSerializer(usersDetails, many=True)
	# return Response(serializer.data)
	# serializer = UserSerializer(usersDetails, many=True)
	# return Response(serializer.data)
	# serializer = UserSerializer(usersDetails, many=True)
	# return Response(serializer.data)
	# serializer = UserSerializer(usersDetails, many=True)
		# return Response(serializer.data)
	# serializer = UserSerializer(usersDetails, many=True)
		
	serializer = UserReadSerializer(usersDetails, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)
	# if request.method == 'GET':
	#     serializer = UserSerializer(usersDetails, many=True)
	#     return Response(serializer.data)
# department: "",
# bank: "",
# branch: "",
# state: "",
# qtyAtm: "",

# uname: "",
# fname: "",
# lname: "",
# mname: "",
# email: "",
# phone: "",
# wphone: "",
# password1: "",
# password2: "",
# address: "",
# aboutme: "",
# ppicture: null,