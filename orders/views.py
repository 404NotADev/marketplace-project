from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer
from .tasks import send_order_confirmation_email


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
       
        return request.user.is_staff or obj.user == request.user


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        send_order_confirmation_email.delay(self.request.user.email, order.id)

#celery -A marketplace worker --loglevel=info
# -A marketplace — имя твоего Django-проекта (папка с settings.py и celery.py)

# worker — команда для запуска воркера

# --loglevel=info — уровень логов (чтобы видеть, что происходит)