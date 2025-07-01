from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Review
from .forms import ReviewForm
from borrow.models import BorrowRequest

class AddReviewView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_success_url(self):
        return reverse_lazy('tool-detail', kwargs={'pk': self.get_rental_request().tool.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rental_request'] = self.get_rental_request()
        return context
    
    def form_valid(self, form):
        rental_request = self.get_rental_request()
        form.instance.rental_request = rental_request
        form.instance.reviewer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Check if user can review this rental."""
        rental_request = self.get_rental_request()
        return (self.request.user == rental_request.borrower and
                rental_request.status == BorrowRequest.Status.COMPLETED and
                not hasattr(rental_request, 'review'))

    def get_rental_request(self):
        return get_object_or_404(BorrowRequest, pk=self.kwargs.get('rental_pk'))