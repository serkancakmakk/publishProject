from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone

# class SessionTimeoutMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             last_activity = request.session.get('last_activity')
#             if last_activity:
#                 timeout_seconds = getattr(settings, 'SESSION_COOKIE_AGE', 13)
#                 if timezone.now() - last_activity > timezone.timedelta(seconds=timeout_seconds):
#                     del request.session['last_activity']
#                     return HttpResponseRedirect('/session-expired/')  # Yönlendirilecek URL
#         response = self.get_response(request)
#         request.session['last_activity'] = timezone.now()
#         return response