import json
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Thread, Message

from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.room_group_name = f'chat_{self.thread_id}'
        self.user = self.scope['user']

        if not self.user.is_authenticated or not await self.is_user_in_thread():
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        new_message = await self.save_message(message)

        formatted_timestamp = timezone.now().strftime('%b %d, %I:%M %p')

        # This block remains. It sends the message to the CHAT window.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': new_message.text,
                'sender': new_message.sender.username,
                'timestamp': formatted_timestamp
            }
        )
        
        # --- ADDED: Real-time notification badge logic ---
        # This new block sends a separate notification to the other user's general notification socket.
        thread = await self.get_thread()
        channel_layer = get_channel_layer()

        # Find all other participants in the thread besides the sender
        other_participants = [p for p in await self.get_thread_participants(thread) if p != self.user]

        # Loop through the other participants and send them a notification
        for participant in other_participants:
            # Construct the group name for their personal notification channel
            group_name = f'user_{participant.id}_notifications'
            await channel_layer.group_send(
                group_name,
                {
                    # This calls the `send_notification` method in our new NotificationConsumer
                    'type': 'send_notification',
                    'notification_type': 'new_message',
                }
            )
        # --- ADDED SECTION END ---

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))
        
    @database_sync_to_async
    def is_user_in_thread(self):
        thread = Thread.objects.filter(pk=self.thread_id).first()
        return thread and self.user in thread.participants.all()

    @database_sync_to_async
    def save_message(self, message_text):
        thread = Thread.objects.get(pk=self.thread_id)
        return Message.objects.create(thread=thread, sender=self.user, text=message_text)

    # --- ADDED: Helper methods to get thread info asynchronously ---
    @database_sync_to_async
    def get_thread(self):
        return Thread.objects.get(pk=self.thread_id)

    @database_sync_to_async
    def get_thread_participants(self, thread):
        return list(thread.participants.all())