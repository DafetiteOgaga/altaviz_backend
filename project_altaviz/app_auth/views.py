from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
# from .models import *
from app_users.serializers import UserReadHandlersSerializer
# from app_bank.serializers import *
from app_custodian.models import Custodian
from app_location.models import Location
# from .serializers import *
from app_users.serializers import UserReadSerializer
from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()

# Create your views here.
@api_view(['POST'])
def loginView(request):
	if request.method == 'POST':
		print(f'login payload: {request.data}')
		email = request.data.get('email')
		password = request.data.get('password')
		print(f'email: {email}\npassword: {password}')
		user = User.objects.get(email=email)
		print(f'user: {user}')
		print(f'user is active: {user.is_active}')
		user = authenticate(email=email, password=password)
		if user:
			print(f'user exists: {user}')
			if user.is_active:
				print(f'user is active: {user.is_active}')
				print(f'user role: 111111111111 {user.role}')
				if user.role == 'custodian':
					print(f'custodian: (views) {Custodian.objects.get(custodian=user)}')
					print(f'custodian.first() (views): {Custodian.objects.first()}')
				login(request, user)
				serializer = UserReadSerializer(user)
				response_data = serializer.data  # Serialized user data
				print(f'user role: 22222222222 {user.role}')
				return Response(response_data, status=status.HTTP_200_OK)
				# return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
			else:
				return Response({"message": "Your account is not active"}, status=status.HTTP_403_FORBIDDEN)
		else:
			return Response({"message": "Invalid credentials"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def logoutView(request):
	if request.method == 'POST':
		logout(request)
		return Response({"message": "Logout from backend successful"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def checkAuth(request):
	print(f'authentication check payload: {request.data}')
	if request.user.is_authenticated:
		user = request.user
		print(f'user: {user}')
		serializer = UserReadSerializer(user)
		# print(f'user serializer: {serializer.data}')
		return Response(serializer.data, status=status.HTTP_200_OK)
		# return Response({"isAuthenticated": True}, status=status.HTTP_200_OK)
	else:
		return Response({"isAuthenticated": False}, status=status.HTTP_401_UNAUTHORIZED)
