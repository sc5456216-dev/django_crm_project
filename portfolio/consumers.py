import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PortfolioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'portfolio_updates'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Handler for skill added event
    async def skill_added(self, event):
        await self.send(text_data=json.dumps({
            'type': 'skill_added',
            'name': event['name']
        }))

    # Handler for project added event
    async def project_added(self, event):
        await self.send(text_data=json.dumps({
            'type': 'project_added',
            'title': event['title'],
            'description': event['description'],
            'slug': event['slug']
        }))