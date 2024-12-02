from django.db import models
import uuid
from .company import Company


# User Model
class User(models.Model):
    TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User')
    ]
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='User')
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.username