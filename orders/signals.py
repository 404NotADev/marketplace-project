from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order, OrderHistory, UserRating
from .tasks import send_order_confirmation_email  


@receiver(pre_save, sender=Order)
def track_order_status_change(sender, instance, **kwargs):
    if instance.pk:
        previous = Order.objects.get(pk=instance.pk)
        if previous.status != instance.status:
            OrderHistory.objects.create(
                order=instance,
                old_status=previous.status,
                new_status=instance.status
            )
            if instance.status == 'delivered':
                rating, _ = UserRating.objects.get_or_create(user=instance.user)
                rating.successful_orders += 1
                rating.save()

           
            if instance.status == 'confirmed':
                send_order_confirmation_email.delay(instance.user.email, instance.id)


