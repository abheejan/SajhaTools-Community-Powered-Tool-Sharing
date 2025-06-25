from django.dispatch import receiver
from allauth.account.signals import user_logged_in

@receiver(user_logged_in)
def handle_user_logged_in(sender, request, user, **kwargs):

    remember = request.POST.get('remember', None)
    
    if remember:
        # User checked 'Remember Me'. Session will use SESSION_COOKIE_AGE from settings.py
        request.session.set_expiry(request.session.get_expiry_age())
        print(f"User {user.username} checked 'Remember Me'. Session set to persistent.")
    else:
        # User did not check 'Remember Me'. Session will expire when the browser closes.
        request.session.set_expiry(0)
        print(f"User {user.username} did not check 'Remember Me'. Session set to expire on browser close.")