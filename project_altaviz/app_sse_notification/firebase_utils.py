from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
import os

# Dynamically construct the path to the credentials file
homePath = os.path.expanduser('~')
firebase_cred_path = os.path.join(homePath, 'firebase-admin.json')

# firebase_utils.py
if not firebase_admin._apps:
	cred = credentials.Certificate(firebase_cred_path)  # Adjust the path
	firebase_admin.initialize_app(cred, {
		"databaseURL": "https://altaviz-notifications-default-rtdb.firebaseio.com/"
	})

def send_notification(message):
	"""
	Send a notification to Firebase Realtime Database.

	Args:
		user_id (int): The ID of the user to notify.
		message (str): The notification message.
	"""
	print('Sending notification to Firebase Realtime Database')
	# print(f'user_id: {user_id}')
	print(f'message: {message}')
	# Define the path in Firebase
	ref = db.reference(f"notifications")
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
		ref.push({
			"message": message,
			"timestamp": datetime.now().isoformat()
		})
		print(f"New notification sent to users.")
	
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
