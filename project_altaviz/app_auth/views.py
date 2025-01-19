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
from app_email.views import sendEmailMethod
from datetime import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
import time

# Generate a unique token
def passwordResetTokenGenerator(user):
	token_generator = PasswordResetTokenGenerator()
	uid = urlsafe_base64_encode(force_bytes(user.pk))  # Encode the user's primary key
	token = token_generator.make_token(user)          # Generate the token
	return uid, token

def sendEmailFxn(data, max_retries=5, delay=5):
	retries = 0
	while retries < max_retries:
		sendEmail = sendEmailMethod(user=data['user'], data=data['payload'])
		if sendEmail != 'error':
			print(f'sendEmail: {sendEmail}')
			return sendEmail  # Exit if successful
		else:
			print(f'Error sending email, retrying... ({retries + 1}/{max_retries})')
			retries += 1
			time.sleep(delay)  # Wait before retrying
	print("Failed to send email after maximum retries.")
	return sendEmail

# Create your views here.
@api_view(['POST'])
def loginView(request):
	if request.method == 'POST':
		print(f'login payload: {request.data}')
		email = request.data.get('email')
		password = request.data.get('password')
		print(f'email: {email}\npassword: {password}')
		user = User.objects.filter(email=email).first()
		print(f'user: {user}')
		if user:
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
					serializedData = UserReadSerializer(user).data
					# response_data = serializer.data  # Serialized user data
					print(f'user role: 22222222222 {user.role}')
					return Response(serializedData, status=status.HTTP_200_OK)
					# return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
				else:
					return Response({"message": "Your account is not active"}, status=status.HTTP_403_FORBIDDEN)
			else:
				return Response({"message": "Oopsy! Invalid credentials"}, status=status.HTTP_404_NOT_FOUND)
		else:
			return Response({"message": "Oops! Account does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def logoutView(request):
	if request.method == 'POST':
		logout(request)
		return Response({"message": "Logout from backend successful"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def changePassword(request, pk=None):
	if request.method == 'POST':
		print(f'change password payload: {request.data}')
		email = request.data.get('email')
		password = request.data.get('oldPassword')
		new_password = request.data.get('password')
		user = User.objects.filter(email=email).first()
		print('email:', email)
		print('password:', password)
		print('New password:', new_password)
		print(f'user: {user}')
		if user:
			user = authenticate(email=email, password=password)
			print(f'auth user: {user}')
			# return Response({'msg': 'change password successful'}, status=status.HTTP_200_OK)
			if user:
				user.set_password(new_password)
				user.save()
				payload = {
					'subject': 'Password Update',
					'message': f'''We noticed that you recently updated your password at exactly {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\nPls, if this is not you, Kindly reach out to our administrator as soon as possible and report this breach to recover your account.\nHowever, ignore this message if it was you was initiated the password update.''',
					# 'recipient': f'{user.email}',
					'heading': 'Password Update Report',
					'support': None, # this should be a link
				}
				sendEmailFxn({'user': user, 'payload': payload})
				return Response({"msg": "Password changed successfully"}, status=status.HTTP_200_OK)
			else:
				return Response({"msg": "Invalid credentials"}, status=status.HTTP_404_NOT_FOUND)
		else:
			return Response({"msg": "Account does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def resetPasswordRequest(request):
	print(f'forgot password payload: {request.data}')
	if request.method == 'POST':
		print(f'forgot password payload: {request.data}')
		email = request.data.get('email')
		FRONTENDURL = request.data.get('FEUrl')
		user = User.objects.filter(email=email).first()
		print(f'email: {email}')
		print(f'FRONTENDURL: {FRONTENDURL}')
		print(f'user: {user}')
		# return Response({"msg": "Password reset email sent successfully"}, status=status.HTTP_200_OK)
		if user:
			uid, token = passwordResetTokenGenerator(user)
			print(f'uid: {uid}\ntoken: {token}')
			currentTimeInMilliseconds = int(time.time() * 1000)
			print(f'currentTimeInMilliseconds: {currentTimeInMilliseconds}')
			resetLink = f"{FRONTENDURL}/reset-password/{uid}/{currentTimeInMilliseconds}/{token}/"
			print(f'resetLink: {resetLink}')
			payload = {
				'subject': 'Password Reset',
				'message': f'''You recently requested for a password reset at exactly {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\nPls, if this is not you, Kindly reach out to our administrator as soon as possible and report this breach to recover your account.\nIf it is you, follow the reset link below.\nNote: This link will expire 3hours.''',
				# 'recipient': f'{user.email}',
				'heading': 'Request Password Reset',
				'support': resetLink
			}
			sendEmailFxn({'user': user, 'payload': payload})
			return Response({"msg": "Password Reset link has been sent to your Email. Check your spam too."}, status=status.HTTP_200_OK)
		else:
			print(f'Account does not exist')
			return Response({"msg": "Account does not exist"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def resetPasswordDone(request, uid, token):
	print(f'payload: {request.data}')
	uid = request.data.get('uid')
	print(f'uid: {uid}')
	token = request.data.get('token')
	print(f'token: {token}')
	new_password = request.data.get('new_password')
	print(f'new_password: {new_password}')
	# return Response({"msg": "Password reset email sent successfully"}, status=status.HTTP_200_OK)
	try:
		user_id = urlsafe_base64_decode(uid).decode()  # Decode the user ID
		print(f'user_id: {user_id}')
		user = User.objects.get(pk=user_id)           # Retrieve the user
		print(f'user: {user}')
		
		token_generator = PasswordResetTokenGenerator()
		print(f'token_generator: {token_generator}')
		if token_generator.check_token(user, token):  # Verify the token
			print(f'Token is valid')
			user.set_password(new_password)           # Set the new password
			user.save()
			print(f'Password reset successful!')
			payload = {
				'subject': 'Password Reset Done',
				'message': f'''You have successfully reset your password at exactly {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\nPls, if this is not you, Kindly reach out to our administrator as soon as possible and report this breach to recover your account.\nHowever, ignore this message if it was you was who initiated the password reset.''',
				# 'recipient': f'{user.email}',
				'heading': 'Password Reset Successful',
				'support': None, # this should be a link
			}
			sendEmailFxn({'user': user, 'payload': payload})
			return Response({"msg": "Password Reset successful!"}, status=status.HTTP_200_OK)
		else:
			print('Invalid or expired token.')
			return Response({"msg": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
	except (User.DoesNotExist, ValueError, TypeError):
		print(f'Invalid request.')
		return Response({"msg": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def checkAuth(request):
	print(f'authentication check payload: {request.data}')
	if request.method == 'POST':
		print(f'beacon received: {request.data}')
		return Response({"beacon": "received"}, status=status.HTTP_200_OK)
	else:
		if request.user.is_authenticated:
			user = request.user
			print(f'user: {user}')
			serializer = UserReadSerializer(user)
			# print(f'user serializer: {serializer.data}')
			return Response(serializer.data, status=status.HTTP_200_OK)
			# return Response({"isAuthenticated": True}, status=status.HTTP_200_OK)
		else:
			return Response({"isAuthenticated": False}, status=status.HTTP_401_UNAUTHORIZED)
