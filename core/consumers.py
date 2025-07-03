import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # A user who is not logged in cannot connect.
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            # All logged-in users are added to their own unique group.
            # The group name is based on their user ID.
            self.room_group_name = f'user_{self.scope["user"].id}_notifications'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # On disconnect, leave the user's personal group.
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # This method is called when we send a message to the group from elsewhere in our code.
    async def send_notification(self, event):
        # Sends the actual message to the WebSocket client.
        await self.send(text_data=json.dumps({
            'type': event['notification_type'],
        }))