from django.urls import path
from .views import (
    ToolListView,
    ToolDetailView,
    ToolCreateView,
    ToolUpdateView,
    ToolDeleteView,
)
from . import views

urlpatterns = [
    path('toolslist/', ToolListView.as_view(), name='tool-list'),
    path('new/', ToolCreateView.as_view(), name='tool-create'),
    path('<int:pk>/', ToolDetailView.as_view(), name='tool-detail'),
    path('<int:pk>/update/', ToolUpdateView.as_view(), name='tool-update'),
    path('<int:pk>/delete/', ToolDeleteView.as_view(), name='tool-delete'),
    path('cart/', views.view_cart, name='view-cart'),
    path('cart/add/<int:tool_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:tool_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/proceed/', views.proceed_to_borrow, name='proceed-to-borrow'),
    path('cart/login-required/', views.cart_login_required, name='cart-login-required'),
]