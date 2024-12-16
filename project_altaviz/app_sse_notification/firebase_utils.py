from datetime import datetime
from firebase_admin import db

def send_notification(user_id, message):
	"""
	Send a notification to Firebase Realtime Database.

	Args:
		user_id (int): The ID of the user to notify.
		message (str): The notification message.
	"""
	print('Sending notification to Firebase Realtime Database')
	print(f'user_id: {user_id}')
	print(f'message: {message}')
	# Define the path in Firebase
	ref = db.reference(f"notifications/{user_id}")
	print(f'the ref data: {ref}')

	# Push and replace the notification in Firebase
	try:
		# Delete old data for the user
		ref.delete()
		print(f"Old notifications for user {user_id} have been deleted.")

		# Push the new notification to Firebase
		ref.push({
			"message": message,
			"timestamp": datetime.now().isoformat()
		})
		print(f"New notification sent for user {user_id}.")
	
	except Exception as e:
		print(f"Error while sending notification for user {user_id}: {e}")


# from myapp.firebase_utils import send_notification

# # Trigger this after a specific event
# send_notification(user_id=123, message="Your task is complete!")
