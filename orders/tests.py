from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch

from .models import Order, OrderItem, OrderHistory
from products.models import ProductsModel

User = get_user_model()

class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='otheruser', password='testpass')
        self.product = ProductsModel.objects.create(
            salesman=self.user,
            category=None,
            title='Test Product',
            price=100.00
        )
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')

    @patch('orders.tasks.send_order_confirmation_email.delay')
    def test_create_order(self, mock_send_email):
        url = reverse('order-list') 

        data = {
            "total_price": "100.00",
            "items": [
                {
                    "product": self.product.id,
                    "quantity": 1,
                    "price": "100.00"
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=response.data['id'])
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.items.count(), 1)
        mock_send_email.assert_called_once_with(self.user.email, order.id)

    def test_order_list_user_only_own(self):
        other_order = Order.objects.create(user=self.user2, total_price=50)
        OrderItem.objects.create(order=other_order, product=self.product, quantity=1, price=50)

        url = reverse('order-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_order_history_created_on_status_change(self):
        order = Order.objects.create(user=self.user, total_price=100, status='pending')
        OrderItem.objects.create(order=order, product=self.product, quantity=1, price=100)

        order.status = 'confirmed'
        order.save()

        history = OrderHistory.objects.filter(order=order)
        self.assertTrue(history.exists())
        self.assertEqual(history.last().old_status, 'pending')
        self.assertEqual(history.last().new_status, 'confirmed')
