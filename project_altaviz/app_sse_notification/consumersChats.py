from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()  # Accept the WebSocket connection
        print("WebSocket connection established!")

    async def disconnect(self, close_code):
        print("WebSocket connection closed!")

    async def receive(self, text_data):
        print(f"Message received: {text_data}")
        data = json.loads(text_data)
        message = data['message']

        # Echo the message back to the client
        await self.send(text_data=json.dumps({
            'message': f"Echo: {message}"
        }))
