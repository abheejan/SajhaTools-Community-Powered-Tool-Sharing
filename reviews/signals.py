from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from .models import Review

@receiver([post_save, post_delete], sender=Review)
def update_tool_rating(sender, instance, **kwargs):

    tool = instance.rental_request.tool
    
    # Calculate the new average rating and count
    reviews = Review.objects.filter(rental_request__tool=tool)
    if reviews.exists():
        # The 'rating' is the field in our Review model we want to average
        aggregation = reviews.aggregate(
            average_rating=Avg('rating'),
            review_count=Count('id')
        )
        tool.average_rating = aggregation.get('average_rating', 0.0)
        tool.review_count = aggregation.get('review_count', 0)
    else:
        # If no reviews exist, reset to defaults
        tool.average_rating = 0.0
        tool.review_count = 0
        
    tool.save()