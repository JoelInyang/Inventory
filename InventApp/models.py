# For the user model we Django’s built-in User model includes fields for username, password, email, first name, and last name, 
# along with fields for staff status and superuser status, which we'll use for role-based access control.
# so for simplicity, we would stick to the built-in User model for now.

from django.conf import settings
from django.db import models

class OutstandingToken(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='user_outstanding_tokens'
    )
    jti = models.UUIDField(db_index=True)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    blacklisted = models.BooleanField(default=False)

    def __str__(self):
        return f"Outstanding token for {self.user}"




from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name



class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = JSONField(default=list)
    #products = JSONField()  # List of {"product_id": 1, "quantity": 2}
    #products = models.ManyToManyField(Product)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
