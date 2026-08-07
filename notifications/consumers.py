import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'notifications_group'

        # Join overall channel group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Optional: Join specific user group if logged in
        if self.scope["user"].is_authenticated:
            self.user_group = f"user_{self.scope['user'].id}"
            await self.channel_layer.group_add(
                self.user_group,
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_discard(
                f"user_{self.scope['user'].id}",
                self.channel_name
            )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'title': event.get('title', 'Notification'),
            'message': event['message'],
            'link': event.get('link', '#'),
            'level': event.get('level', 'info'),
        }))