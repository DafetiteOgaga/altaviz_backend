from django.urls import path
from .consumersChats import ChatConsumer
from .consumersNotification import NotificationConsumer

websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi()),  # Example WebSocket endpoint
    path('ws/notifications/', NotificationConsumer.as_asgi()),
]