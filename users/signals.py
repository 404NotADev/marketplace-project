from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserActionLog

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserActionLog.objects.create(
        user=user,
        action='login',
        description=f'Вход выполнен с IP: {get_client_ip(request)}'
    )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')
