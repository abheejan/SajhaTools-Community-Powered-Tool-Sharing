from .signals import request_approved
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View

from .models import BorrowRequest
from .forms import BorrowRequestForm
from tools.models import Tool
from borrow.models import BorrowRequest

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class BorrowRequestCreateView(LoginRequiredMixin, CreateView):
    model = BorrowRequest
    form_class = BorrowRequestForm
    template_name = 'borrow/borrow_request_form.html' 
    success_url = reverse_lazy('request-dashboard') # Redirect to their dashboard after request

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the tool object to the template
        context['tool'] = get_object_or_404(Tool, pk=self.kwargs['tool_pk'])
        return context

    def form_valid(self, form):
        # Assign the tool and borrower automatically
        tool = get_object_or_404(Tool, pk=self.kwargs['tool_pk'])
        form.instance.tool = tool
        form.instance.borrower = self.request.user
        response = super().form_valid(form)

        # Remove this tool from the cart
        cart = self.request.session.get('cart', [])
        if str(tool.pk) in cart:
            cart.remove(str(tool.pk))
        elif tool.pk in cart:
            cart.remove(tool.pk)
        self.request.session['cart'] = cart

        # If there are more tools in the cart, redirect to the next one's request form
        if cart:
            next_tool_id = cart[0]
            return redirect('borrow-request-create', tool_pk=next_tool_id)

        tool_owner = tool.owner
        
        
        channel_layer = get_channel_layer()
        
    
        group_name = f'user_{tool_owner.id}_notifications'
        
    
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification',
                'notification_type': 'new_borrow_request',
            }
        )
        return response 
    

class RequestDashboardView(LoginRequiredMixin, ListView):
    model = BorrowRequest
    template_name = 'borrow/request_dashboard.html'
    context_object_name = 'requests' # This name is a bit ambiguous, we'll fix in get_context_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Requests made by the current user
        context['my_borrow_requests'] = BorrowRequest.objects.filter(borrower=user).order_by('-request_date')
        
        # Requests for tools owned by the current user
        context['incoming_tool_requests'] = BorrowRequest.objects.filter(tool__owner=user).order_by('-request_date')

        return context
    
class UpdateRequestStatusView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        request_pk = self.kwargs['pk']
        action = request.POST.get('action') # 'approve' or 'deny'
        
        borrow_request = get_object_or_404(BorrowRequest, pk=request_pk)
        
        # Security Check: only the tool owner can approve/deny
        if borrow_request.tool.owner != request.user:
            return HttpResponseForbidden("You are not authorized to perform this action.")
            
        if action == 'approve':
            borrow_request.status = BorrowRequest.Status.APPROVED
            borrow_request.approved_date = timezone.now()

            # Send a signal to notify the tool owner
            request_approved.send(sender=self.__class__, borrow_request=borrow_request)
            
        elif action == 'deny':
            borrow_request.status = BorrowRequest.Status.DENIED
            borrow_request.denied_date = timezone.now()

        elif action == 'complete':
            if borrow_request.status == BorrowRequest.Status.APPROVED:
                borrow_request.status = BorrowRequest.Status.COMPLETED
                tool = borrow_request.tool
                tool.availability_status = Tool.Availability.AVAILABLE
                tool.save()

        borrow_request.save()
        
        return redirect('request-dashboard')