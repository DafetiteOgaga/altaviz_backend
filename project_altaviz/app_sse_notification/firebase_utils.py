from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db, initialize_app, _apps
import os

# Dynamically construct the path to the credentials file
homePath = os.path.expanduser('~')
firebase_cred_path = os.path.join(homePath, 'firebase')

notification_db = None
chats_db = None
# notifications
# if not firebase_admin._apps:


# Check and initialize notification app
if "notification_db" not in _apps:
	cred_notification = credentials.Certificate(f'{firebase_cred_path}/altaviz-app-notification.json')  # Adjust the path
	notification_db = firebase_admin.initialize_app(cred_notification, {
		"databaseURL": "https://altaviz-notifications-default-rtdb.firebaseio.com/"
	}, name="notification_db")

# Check and initialize chat app
if "chats_db" not in _apps:
	cred_chats = credentials.Certificate(f'{firebase_cred_path}/altaviz-chat-notification.json')  # Adjust the path
	chats_db = firebase_admin.initialize_app(cred_chats, {
		"databaseURL": "https://altaviz-chat-notification-default-rtdb.firebaseio.com/"
	}, name="chats_db")


def send_notification(message):
	print('Sending notification to Firebase Realtime Database')
	# print(f'user_id: {user_id}')
	print(f'message: {message}')
	notification_data = {
		"message": message,
		"timestamp": datetime.now().isoformat()
	}
	# Define the path in Firebase
	ref = db.reference(f"notifications", app=notification_db)
	print(f'the referenced location: {ref}')
	data = ref.get()
	print("Data at the reference:", data)  # Prints the data stored at the reference
	dataKey = next(iter(data.keys()), None) if data else None # gets the first key from the reference dict

	# Push and replace the notification in Firebase
	try:
		# Delete old data for the user
		ref.delete()
		print(f"Old notifications for {dataKey} have been deleted.")

		# Push the new notification to Firebase
		ref.push(notification_data)
		print(f"New notification sent to users.")
	except Exception as e:
		print(f"Error while sending notification to users: {e}")


def send_chat_notification(senderID, receiverID, message, senderName, receiverName):
	print(f'Sending chat notifications from {senderName} to {receiverName} using Firebase Realtime Database')
	# print(f'user_id: {user_id}')
	print(f'message: {message}')
	# Define the path in Firebase
	ref = db.reference(f"chat-notifications/{receiverID}", app=chats_db)
	print(f'the referenced location: {ref}')
	data = ref.get()
	print("Data at the reference:", data)  # Prints the data stored at the reference
	counter = 0
	dataKey = None
	senders = {}
	listKeys = None
	if data:
		dataKey = next(iter(data.keys()), None) if data else None # gets the first key from the reference dict
		print(f'dataKey: {dataKey}')
		listKeys = str(senderID) in data[dataKey]['sendersList'].keys()
		print(f'senderID: {senderID}')
		print(f'previous sender: {listKeys}')
		if listKeys:
			# counter = data[dataKey]['sendersList'][senderID]['notificationCount']
			counter = data[dataKey]['sendersList'][f'{senderID}']['notificationCount']
		senders = data[dataKey]['sendersList']
	print(f'counter: {counter+1}')
	print(f'senders: {senders}')
	notification_data = {
		"receiverID": receiverID,
		'sendersList': {
			**senders,
			**{senderID: {'notificationCount': counter + 1}}
		},
		"notificationTimestamp": datetime.now().isoformat()
	}

	# Push and replace the notification in Firebase
	try:
		# Delete old data for the user
		ref.delete()
		print(f"Old notifications for {dataKey} have been deleted.")

		# Push the new notification to Firebase
		ref.push(notification_data)
		print(f"New notification sent to {receiverName}.")
	
	except Exception as e:
		print(f"Error while sending notification to users: {e}")




# def send_notification(user_id, message):
# 	"""
# 	Send a notification to Firebase Realtime Database.

# 	Args:
# 		user_id (int): The ID of the user to notify.
# 		message (str): The notification message.
# 	"""
# 	print('Sending notification to Firebase Realtime Database')
# 	print(f'user_id: {user_id}')
# 	print(f'message: {message}')
# 	# Define the path in Firebase
# 	ref = db.reference(f"notifications/{user_id}")
# 	print(f'the referenced location: {ref}')
# 	data = ref.get()
# 	print("Data at the reference:", data)  # Prints the data stored at the reference

# 	# Push and replace the notification in Firebase
# 	try:
# 		# Delete old data for the user
# 		ref.delete()
# 		print(f"Old notifications for user {user_id} have been deleted.")

# 		# Push the new notification to Firebase
# 		ref.push({
# 			"message": message,
# 			"timestamp": datetime.now().isoformat()
# 		})
# 		print(f"New notification sent for user {user_id}.")
	
# 	except Exception as e:
# 		print(f"Error while sending notification for user {user_id}: {e}")


# from myapp.firebase_utils import send_notification

# # Trigger this after a specific event
# send_notification(user_id=123, message="Your task is complete!")
