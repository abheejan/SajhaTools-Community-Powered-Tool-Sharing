from django.urls import path
from .views import (
    ToolListView,
    ToolDetailView,
    ToolCreateView,
    ToolUpdateView,
    ToolDeleteView,
)

urlpatterns = [
    path('toolslist/', ToolListView.as_view(), name='tool-list'),
    path('new/', ToolCreateView.as_view(), name='tool-create'),
    path('<int:pk>/', ToolDetailView.as_view(), name='tool-detail'),
    path('<int:pk>/update/', ToolUpdateView.as_view(), name='tool-update'),
    path('<int:pk>/delete/', ToolDeleteView.as_view(), name='tool-delete'),
]