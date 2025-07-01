from django.urls import path
from .views import AddReviewView

urlpatterns = [
    # URL for adding a review to a specific completed rental
    path('rental/<int:rental_pk>/add/', AddReviewView.as_view(), name='add-review'),
]