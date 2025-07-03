from borrow.models import BorrowRequest
from messaging.models import Thread

def notification_counts(request):
    """
    Provides notification counts for the currently logged-in user.
    """
    if not request.user.is_authenticated:
        return {} # Return an empty dict if the user is not logged in

    # 1. Count of new incoming Borrow requests
    incoming_request_count = BorrowRequest.objects.filter(
        tool__owner=request.user, 
        status=BorrowRequest.Status.PENDING
    ).count()

    # 2. Count of unread message threads
    # A thread is unread if its last message was not sent by the current user and is_read is False.
    # This logic can be refined, but it's a good starting point.
    # For a more robust solution, you might add an 'unread_by' ManyToManyField on the Message model.
    unread_threads_count = request.user.chat_threads.filter(
        messages__is_read=False
    ).exclude(
        messages__sender=request.user
    ).distinct().count()

    # 3. Count of pending reviews the user needs to write
    pending_review_count = BorrowRequest.objects.filter(
        borrower=request.user,
        status=BorrowRequest.Status.COMPLETED,
        review__isnull=True  # Check if a review does not exist for this Borrow
    ).count()

    total_notifications = incoming_request_count + unread_threads_count + pending_review_count
    
    return {
        'incoming_request_count': incoming_request_count,
        'unread_threads_count': unread_threads_count,
        'pending_review_count': pending_review_count,
        'total_notifications': total_notifications,
    }