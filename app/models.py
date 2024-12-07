from django.db import models
from datetime import date



# Address Model
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"


# Company Model
class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    location = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='company_images/', blank=True, null=True)

    def __str__(self):
        return self.name

# User Model
class User(models.Model):
    TYPE_CHOICES = [
        ('Company User', 'Company User'),
        ('Company Admin', 'Company Admin'),
        ('System Admin', 'System Admin'),
    ]
    username = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=30, choices=TYPE_CHOICES, default='User')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

# Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.ForeignKey(Address, related_name="address", on_delete=models.SET_NULL, null=True)
    billing_address = models.ForeignKey(Address, related_name="billing_address", on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", on_delete=models.SET_NULL, null=True)
    account_status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Fire Extinguisher Model
class FireExtinguisher(models.Model):
    TYPE_CHOICES = [
        ('Water', 'Water'),
        ('Water Mist', 'Water Mist'),
        ('Foam', 'Foam'),
        ('CO2', 'CO2'),
        ('Powder', 'Powder'),
        ('Wet Chemical', 'Wet Chemical'),
    ]

    FIRE_CLASS_CHOICES = [
        ('Class A', 'Class A'),
        ('Class B', 'Class B'),
        ('Class C', 'Class C'),
        ('Class D', 'Class D'),
        ('Class F', 'Class F'),
        ('Electrical Fires', 'Electrical Fires'),
    ]

    CERTIFICATION_CHOICES = [
        ('CE Marking', 'CE Marking'),
        ('UL', 'UL'),
        ('FM', 'FM'),
        ('BSI Kitemark', 'BSI Kitemark'),
        ('EN3', 'EN3'),
        ('DIN', 'DIN'),
        ('NFPA', 'NFPA'),
        ('AS', 'AS'),
        ('ISI Mark', 'ISI Mark'),
        ('TUV', 'TUV'),
        ('ISO', 'ISO'),
    ]

    STANDARDS_COMPLIANCE_CHOICES = [
        ('EN3', 'EN3'),
        ('ISO_9001', 'ISO_9001'),
        ('NFPA_10', 'NFPA_10'),
        ('NFPA_17', 'NFPA_17'),
        ('BS EN_1866', 'BS EN_1866'),
        ('ANSI UL_299', 'ANSI UL_299'),
        ('ISO_11602', 'ISO_11602'),
        ('AS_2444', 'AS_2444'),
        ('JIS', 'JIS'),
        ('CCC', 'CCC'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    fire_extinguisher_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    fire_class = models.CharField(max_length=20, choices=FIRE_CLASS_CHOICES)
    certification = models.CharField(max_length=50, choices=CERTIFICATION_CHOICES)
    standards_compliance = models.CharField(max_length=50, choices=STANDARDS_COMPLIANCE_CHOICES)
    capacity = models.PositiveIntegerField()
    inspection_date = models.DateField()
    service_date = models.DateField()
    expiry_date = models.DateField()
    manufacture_date = models.DateField()
    inventory = models.PositiveIntegerField()
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    warranty_period = models.PositiveIntegerField(help_text="Warranty period in months")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.name} ({self.type})"


# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
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
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.fire_extinguisher.name}"
