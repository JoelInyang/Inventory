from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Product, Order

class InventoryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(email='admin@example.com', password='admin123', is_staff=True)
        self.regular_user = User.objects.create_user(email='user@example.com', password='user123', is_staff=False)
        self.product = Product.objects.create(name='Test Product', description='Test Description', quantity=20, price=100)

    def test_user_registration(self):
        url = reverse('user-signup')
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        url = reverse('user-login')
        data = {
            'email': 'user@example.com',
            'password': 'user123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_product_creation(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('product-create')
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'quantity': 15,
            'price': 50
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_product_update(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('product-update', args=[self.product.id])
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'quantity': 10,
            'price': 80
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_product_deletion(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('product-delete', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_order_creation(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('order-create')
        data = {
            'items': [{'product_id': self.product.id, 'quantity': 2}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_order_status_update(self):
        self.client.force_authenticate(user=self.admin_user)
        order = Order.objects.create(user=self.regular_user, status='pending', items=[{'product_id': self.product.id, 'quantity': 2}])
        url = reverse('order-status-update', args=[order.id])
        data = {'status': 'completed'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, 'completed')
