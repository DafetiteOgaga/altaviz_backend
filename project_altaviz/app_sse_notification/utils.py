from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_websocket_notification(message):
    """
    Sends a notification to all WebSocket clients in the 'notification_group'.
    """
    print('send_websocket_notification ##########')
    print(f'sending: {message} ##########')
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_group",  # Group name
        {
            "type": "websocket_send_notification",  # Refers to the method in `consumerNotification`
            "message": message
        }
    )
    print(f"Dispatched message to notification_group: {message}")

