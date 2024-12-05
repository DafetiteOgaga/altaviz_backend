# from django.shortcuts import render
# from django.http import StreamingHttpResponse
# from threading import Thread, Event
# import time, requests
# from time import sleep

# # Create your views here.

# # A global event to trigger notifications
# notification_event = Event()

# # A global variable to store the latest message to be sent
# latest_message = "No new notifications"

# # Function to stream notifications to connected clients
# def event_stream():
# 	global latest_message
# 	while True:
# 		# Wait until there is a new notification
# 		notification_event.wait()  # Pauses until `notification_event.set()` is called
# 		# time.sleep(3)
# 		yield f"data: {latest_message}\n\n"
# 		notification_event.clear()  # Reset the event to pause until next notification

# # View for handling SSE notifications
def sse_notification_view(request):
    pass
# 	print(f'sending SSE notification ... ##### {time.ctime()} #####')
# 	response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
# 	response['Cache-Control'] = 'no-cache'
# 	response['X-Accel-Buffering'] = 'no'
# 	response['Access-Control-Allow-Origin'] = 'http://localhost:3000'  # Your frontend URL
# 	# response['Access-Control-Allow-Credentials'] = 'true'
# 	response["Access-Control-Allow-Methods"] = "GET"
# 	response["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With"
# 	print(f'response: {response}')
# 	return response

# # Helper function to trigger SSE notifications from other views
# def send_sse_notification(message):
# 	global latest_message
# 	print(f'sendng: {message} to frontend #####')
# 	latest_message = message
# 	notification_event.set()  # Notify the `event_stream` to send the latest message

# 	# try:
# 	# 	sse_server_url = "http://127.0.0.1:8001/sse-endpoint/"  # Replace with your SSE server's endpoint
# 	# 	response = requests.post(sse_server_url, json={"message": message})
# 	# 	response.raise_for_status()  # Check for HTTP errors
# 	# 	print(f"Message sent to external SSE server successfully: {response.status_code}")
# 	# except requests.exceptions.RequestException as e:
# 	# 	print(f"Error sending message to external SSE server: {e}")
