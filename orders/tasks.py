from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_order_confirmation_email(user_email, order_id):
    subject = f'Подтверждение заказа #{order_id}'
    message = f'Спасибо за ваш заказ! Ваш номер заказа: {order_id}. Мы скоро свяжемся с вами.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
