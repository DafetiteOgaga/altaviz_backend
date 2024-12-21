from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Chat
from app_users.models import User
from .serializers import ChatsSerializer
import json
from django.db.models import Q

# Create your views here.
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def chatUser(request, cpk=None, upk=None):
	print(f'upk: {upk}')
	print(f'cpk: {cpk}')
	print(f'{request.method} method')
	print(f'Payload: {request.data}')
	contact = User.objects.filter(id=cpk).first()
	if not contact:
		return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)

	user = User.objects.get(pk=upk)
	print(f'user: {user}')

	# Fetch all messages between user A and user B, regardless of direction
	chats = Chat.objects.filter(
		Q(user=user, contact=contact) | Q(user=contact, contact=user)
	).order_by('-timestamp')  # Order chronologically (oldest to newest)
	print(f'raw query: {chats.query}')
	data = request.data.copy()
	# if not backwardChatsExist:
	# 	# Use the "forward" direction
	# 	if request.method == 'POST': data['youMessage'] = request.data['msg']
	# 	chats = Chat.objects.filter(user=user, contact=contact).order_by('-timestamp')
	# 	print(f'chats 01 > : {chats}')
	# 	if chats: print(f'chats 01 > : {chats.first()}, youMsg: {chats.first().youMessage}, contactMsg: {chats.first().contactMessage}')
	# 	# print(f'checking: youMessage: {chats[0].yourMessage} and contactMessage: {chats[0].contactMessage}')
	# else:
	# 	# Use the "backward" direction (user=contact, contact=user)
	# 	if request.method == 'POST': data['contactMessage'] = request.data['msg']
	# 	chats = Chat.objects.filter(user=contact, contact=user).order_by('-timestamp')
	# 	print(f'chats 02 < : {chats}')
	# 	if chats: print(f'chats 02 < : {chats.first()}, youMsg: {chats.first().youMessage}, contactMsg: {chats.first().contactMessage}')
	# 	# print(f'checking: youMessage: {chats[0].yourMessage} and contactMessage: {chats[0].contactMessage}')

	# chatsForward = Chat.objects.filter(user=user, contact=contact).order_by('-timestamp')
	# chatsBackward = Chat.objects.filter(user=contact, contact=user).order_by('-timestamp')
	# chats = chatsForward | chatsBackward
	print(f'your chats with {contact.first_name}: {chats}')
	if request.method == 'GET':
		if not chats.exists():
			startingChats = [{
				'user': {'first_name': user.first_name},
				'contact': {'first_name': contact.first_name},
				'message': None,  # Use Python's None to represent null in JSON
				'timestamp': None
			}]
			# Convert Python list to JSON
			startingChatsJson = json.dumps(startingChats)
			print(f'startingChatsJson: {startingChatsJson}')
			print('############### NEW done ###############')
			return Response(startingChats, status=status.HTTP_200_OK)
		serializedChats = ChatsSerializer(instance=chats, many=True).data
		print('chats:')
		[print(f'''{msg.contact.first_name if msg.message.split("=")[0]==msg.contact.username else msg.user.first_name}: {msg.message.split('=')[1]}''') for msg in chats]
		print('############### GET done ###############')
		return Response(serializedChats, status=status.HTTP_200_OK)
	elif request.method == 'POST':
		# data = request.data.copy()
		data['user'] = user.id
		print(f'data: {data}')
		serializer = ChatsSerializer(data=data)
		if serializer.is_valid():
			newChat = serializer.save(user=user, contact=contact)
			print('saved chat #############')
			serializedChats = ChatsSerializer(instance=newChat).data
			serializedChats = list(serializedChats)[::-1]
			# print(f'Serialized Chat: {serializedChats}')
			print('chats:')
			[print(f'''{msg.contact.first_name if msg.message.split('=')[0]==msg.contact.username else msg.user.first_name}: {msg.message.split("=")[1]}''') or None for msg in chats]
			print('############### POST done ###############')
			return Response(serializedChats, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'PATCH':
		# if not chats.exists():
		# 	return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)

		# chat_instance = chats.first()
		# serializer = ChatsSerializer(instance=chat_instance, data=request.data, partial=True)
		# if serializer.is_valid():
		# 	updated_chat = serializer.save()
		# 	serializedChat = ChatsSerializer(instance=updated_chat).data
		# 	print(f'Serialized Chat: {serializedChat}')
		# 	return Response(serializedChat, status=status.HTTP_200_OK)
		# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		pass

	elif request.method == 'DELETE':
		# if not chats.exists():
		# 	return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)

		# chats.delete()
		# return Response({'message': 'Chat deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
		pass