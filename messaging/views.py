from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Thread, Message

User = get_user_model()

class ThreadListView(LoginRequiredMixin, ListView):
    model = Thread
    template_name = 'messaging/thread_list.html'
    context_object_name = 'threads'
    
    def get_queryset(self):
        # Return threads that the current user is a participant in
        return Thread.objects.filter(participants=self.request.user)

class ThreadDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        thread = get_object_or_404(Thread, pk=pk, participants=request.user)
        messages_to_mark_as_read = thread.messages.exclude(sender=request.user)
        messages_to_mark_as_read.update(is_read=True)
        
        messages = thread.messages.all().order_by('timestamp')
        return render(request, 'messaging/thread_detail.html', {'thread': thread, 'messages': messages})

class StartChatView(LoginRequiredMixin, View):
    def get(self, request, user_pk):
        # Avoid creating a chat with oneself
        other_user = get_object_or_404(User, pk=user_pk)
        if other_user == request.user:
            # Maybe redirect to the user's own profile or homepage
            return redirect('home')
        
        # Use our custom manager method to find or create the thread
        thread = Thread.objects.get_or_create_thread(request.user, other_user)
        return redirect('thread-detail', pk=thread.pk)