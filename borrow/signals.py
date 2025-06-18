import django.dispatch

# Signal sent when a rental request is approved
request_approved = django.dispatch.Signal()