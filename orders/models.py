from django.db import models
from django.contrib.auth import get_user_model
from products.models import ProductsModel

# Create your models here.
# orders/models.py


User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('confirmed', 'Подтвержден'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order.id}: {self.old_status} → {self.new_status}"


class UserRating(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    successful_orders = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} — {self.successful_orders} успешных заказов"
