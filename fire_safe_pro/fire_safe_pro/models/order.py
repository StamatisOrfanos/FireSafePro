from django.db import models
import uuid
from datetime import date, timedelta
from .fire_extinguisher import FireExtinguisher
from .customer import Customer


# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"

# OrderItem Model to handle the many-to-many relationship between Orders and FireExtinguishers
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    fire_extinguisher = models.ForeignKey(FireExtinguisher, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.fire_extinguisher.name} in Order {self.order.order_id}"