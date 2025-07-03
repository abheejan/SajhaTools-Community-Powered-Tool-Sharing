import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Thread, Message

# --- ADDED: Import Django's timezone utility ---
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.room_group_name = f'chat_{self.thread_id}'
        self.user = self.scope['user']

        # Security check: User must be authenticated and a participant
        if not self.user.is_authenticated or not await self.is_user_in_thread():
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # --- MODIFIED: The receive method is corrected here ---
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save message to DB. This part is correct.
        new_message = await self.save_message(message)

        # Create a reliable, formatted timestamp *before* sending.
        formatted_timestamp = timezone.now().strftime('%b %d, %I:%M %p')

        # Send message to room group using our new timestamp.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': new_message.text, # This is safe to use
                'sender': new_message.sender.username, # This is safe to use
                'timestamp': formatted_timestamp # This is the corrected line
            }
        )

    async def chat_message(self, event):
        # This method is unchanged as it correctly forwards the payload.
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))
        
    @database_sync_to_async
    def is_user_in_thread(self):
        # This method is unchanged and correct.
        thread = Thread.objects.filter(pk=self.thread_id).first()
        return thread and self.user in thread.participants.all()

    @database_sync_to_async
    def save_message(self, message_text):
        # This method is unchanged and correct.
        thread = Thread.objects.get(pk=self.thread_id)
        return Message.objects.create(thread=thread, sender=self.user, text=message_text)