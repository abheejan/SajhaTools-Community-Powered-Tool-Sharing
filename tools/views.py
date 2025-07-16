from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tool
from .forms import ToolForm
from borrow.models import BorrowRequest
from django.utils import timezone
from django.db import models

class ToolListView(ListView):
    model = Tool
    template_name = 'tools/tool_list.html' 
    context_object_name = 'tools'
    ordering = ['-availability_status', '-posted_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Exclude current user's own tools if authenticated
        if self.request.user.is_authenticated:
            queryset = queryset.exclude(owner=self.request.user)
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                models.Q(name__icontains=q) | models.Q(description__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '').strip()
        return context


class ToolDetailView(DetailView):
    model = Tool
    template_name = 'tools/tool_detail.html' 
    context_object_name = 'tool'


class ToolCreateView(LoginRequiredMixin, CreateView):
    """View for users to post a new tool."""
    model = Tool
    form_class = ToolForm
    template_name = 'tools/tool_form.html' 

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ToolUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for tool owners to update their tool listing."""
    model = Tool
    form_class = ToolForm
    template_name = 'tools/tool_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Ensure the user trying to update the tool is the owner."""
        tool = self.get_object()
        return self.request.user == tool.owner


class ToolDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for tool owners to delete their tool listing."""
    model = Tool
    template_name = 'tools/tool_confirm_delete.html' 
    success_url = reverse_lazy('tool-list')

    def test_func(self):
        """Ensure the user trying to delete the tool is the owner."""
        tool = self.get_object()
        return self.request.user == tool.owner

def add_to_cart(request, tool_id):
    cart = request.session.get('cart', [])
    if tool_id not in cart:
        cart.append(tool_id)
        request.session['cart'] = cart
        messages.success(request, 'Tool added to cart!')
    else:
        messages.info(request, 'Tool is already in your cart.')
    return redirect(request.META.get('HTTP_REFERER', 'tool-list'))

def remove_from_cart(request, tool_id):
    cart = request.session.get('cart', [])
    if tool_id in cart:
        cart.remove(tool_id)
        request.session['cart'] = cart
        messages.success(request, 'Tool removed from cart.')
    return redirect('view-cart')

def view_cart(request):
    cart = request.session.get('cart', [])
    tools = Tool.objects.filter(id__in=cart)
    return render(request, 'tools/cart.html', {'tools': tools})

def cart_login_required(request):
    return render(request, 'tools/cart_login_required.html')

@login_required
def proceed_to_borrow(request):
    cart = request.session.get('cart', [])
    if not cart:
        messages.info(request, 'Your cart is empty.')
        return redirect('view-cart')
    first_tool_id = cart[0]
    return redirect('borrow-request-create', tool_pk=first_tool_id)

@login_required
def my_tools(request):
    tools = Tool.objects.filter(owner=request.user)
    q = request.GET.get('q', '').strip()
    if q:
        tools = tools.filter(
            models.Q(name__icontains=q) | models.Q(description__icontains=q)
        )
    return render(request, 'tools/my_tools.html', {'tools': tools, 'search_query': q})