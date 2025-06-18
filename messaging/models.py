from django.db import models
from django.conf import settings
from django.db.models import Q

class ThreadManager(models.Manager):
    def get_or_create_thread(self, user1, user2):
        """Finds or creates a chat thread between two users."""
        # Q objects allow for complex queries, here we check for either user order
        threads = self.get_queryset().filter(
            Q(participants=user1) & Q(participants=user2)
        )
        if threads.exists():
            return threads.first()
        else:
            thread = self.create()
            thread.participants.add(user1, user2)
            return thread

class Thread(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_threads')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = ThreadManager()

    class Meta:
        ordering = ['-updated']

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} in Thread {self.thread.id}"
    
    class Meta:
        ordering = ['timestamp']