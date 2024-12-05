from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
	print(f"connecting ... ###############")
	connected_users = {}  # Class variable to track connected users

	async def connect(self):
		# Add client to a group for broadcasting notifications
		await self.channel_layer.group_add(
			"notification_group",  # Group name
			self.channel_name      # Client's channel name
		)
		await self.accept()  # Accept the WebSocket connection
		self.send(text_data=json.dumps({"message": "WebSocket connected!"}))
		# print(f"Client connected: {self.channel_name} ################")
		# Debug log for connection
		# print(f"Client connected: {self.channel_name} added to notification_group ################")
		
		# Track the connected user
		self.__class__.connected_users[self.channel_name] = self.scope.get("user", "Anonymous")
		print(f"Currently connected users:")
		for index, user in enumerate(self.__class__.connected_users.values()):
			print(f'{index+1}. {hex(id(user))}')
		print(f'total users: {len(self.__class__.connected_users)}')

	async def disconnect(self, close_code):
		# Remove client from the group when the WebSocket disconnects
		await self.channel_layer.group_discard(
			"notification_group",
			self.channel_name
		)
		# print(f"Remaining connected users:")
		# for index, user in enumerate(self.__class__.connected_users.values()):
		# 	print(f'{index+1}. {hex(id(user))}')
		# print(f'total users: {len(self.__class__.connected_users)}')
		
		# Remove the user from tracking
		self.__class__.connected_users.pop(self.channel_name, None)
		print(f"Remaining connected users:")
		for index, user in enumerate(self.__class__.connected_users.values()):
			print(f'{index+1}. {hex(id(user))}')
		print(f'total users: {len(self.__class__.connected_users)}')

	async def websocket_send_notification(self, event):
		# Send the notification to the WebSocket client
		print('websocket_send_notification ##########')
		print(f"Received event in websocket_send_notification: {event}")
		print(f'sending: {event["message"]} to clients ##########')
		print(f"Connected users:")
		for index, user in enumerate(self.__class__.connected_users.values()):
			print(f'{index+1}. {hex(id(user))}')
		print(f'total users: {len(self.__class__.connected_users)}')
		await self.send(text_data=json.dumps({
			"message": event["message"]  # Message sent from the backend
		}))
