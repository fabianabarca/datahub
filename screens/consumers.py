import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Screen
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


class ScreenConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.screen_id = self.scope["url_route"]["kwargs"]["screen_id"]
        self.screen_group_name = f"screen_{self.screen_id}"

        await self.channel_layer.group_add(self.screen_group_name, self.channel_name)
        await self.accept()
        await self.activate_screen(self.screen_id)

    @sync_to_async
    def activate_screen(self, screen_id):
        screen = Screen.objects.get(screen_id=screen_id)
        screen.is_active = True
        print(f"Screen {screen_id} is now active")
        screen.save()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.screen_group_name, self.channel_name
        )
        await self.deactivate_screen(self.screen_id)

    @sync_to_async
    def deactivate_screen(self, screen_id):
        screen = Screen.objects.get(screen_id=screen_id)
        screen.is_active = False
        print(f"Screen {screen_id} is now inactive")
        screen.save()

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.screen_group_name, {"type": "screen.message", "message": message}
        )

    # Send message to WebSocket
    async def screen_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
