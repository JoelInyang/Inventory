from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Product, Order

class InventoryTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')
        self.product1 = Product.objects.create(name='Product 1', description='Description 1', quantity=10, price=100)
        self.product2 = Product.objects.create(name='Product 2', description='Description 2', quantity=20, price=200)

    def test_user_signup(self):
        signup_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword"
        }
        response = self.client.post('/signup/', signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_user_login(self):
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        response = self.client.post('/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data['data'])
        self.assertIn('refresh_token', response.data['data'])

    def test_order_creation(self):
        self.client.force_authenticate(user=self.user)
        order_data = {
            "products": [
                {
                    "product_id": self.product1.id,
                    "quantity": 5
                },
                {
                    "product_id": self.product2.id,
                    "quantity": 10
                }
            ]
        }
        response = self.client.post('/orders-create/', order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.products, order_data['products'])

    def test_product_creation(self):
        self.client.force_authenticate(user=self.admin_user)
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "quantity": 50,
            "price": 500
        }
        response = self.client.post('/products-create/', product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
        product = Product.objects.get(name="New Product")
        self.assertEqual(product.description, "New Description")
        self.assertEqual(product.quantity, 50)
        self.assertEqual(product.price, 500)

    def test_product_update(self):
        self.client.force_authenticate(user=self.admin_user)
        update_data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "quantity": 30,
            "price": 300
        }
        response = self.client.put(f'/products-update/{self.product1.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product = Product.objects.get(id=self.product1.id)
        self.assertEqual(product.name, "Updated Product")
        self.assertEqual(product.description, "Updated Description")
        self.assertEqual(product.quantity, 30)
        self.assertEqual(product.price, 300)

    def test_product_deletion(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/products-delete/{self.product1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)

    def test_product_listing(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
