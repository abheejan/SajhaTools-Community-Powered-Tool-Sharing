# Update imports and urlpatterns
from django.urls import path
from .views import (
    BorrowRequestCreateView, 
    RequestDashboardView, 
    UpdateRequestStatusView,
)

urlpatterns = [
    path('request/tool/<int:tool_pk>/', BorrowRequestCreateView.as_view(), name='borrow-request-create'),
    path('dashboard/', RequestDashboardView.as_view(), name='request-dashboard'),
    path('request/<int:pk>/update/', UpdateRequestStatusView.as_view(), name='request-update-status'),
]