from django.urls import path
from .views import ThreadListView, ThreadDetailView, StartChatView

urlpatterns = [
    path('', ThreadListView.as_view(), name='thread-list'),
    path('thread/<int:pk>/', ThreadDetailView.as_view(), name='thread-detail'),
    path('start-chat/<int:user_pk>/', StartChatView.as_view(), name='start-chat'),
]