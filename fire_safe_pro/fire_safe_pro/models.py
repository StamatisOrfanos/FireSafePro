from django.db import models
import uuid
from datetime import date, timedelta



# Company Model
class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


# Address Model
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"

# Customer Model
class Customer(models.Model):
    ACCOUNT_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    customer_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='primary_address')
    billing_address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='billing_address')
    shipping_address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipping_address')
    account_status = models.CharField(max_length=10, choices=ACCOUNT_STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    companies = models.ManyToManyField(Company, related_name='customers')

    def __str__(self):
        return self.name
    
    def total_extinguishers_by_type(self):
        # Calculate total extinguishers owned by this customer, grouped by type
        extinguisher_counts = {}
        orders = self.orders.all()
        for order in orders:
            for item in order.items.all():
                extinguisher_type = item.fire_extinguisher.type
                if extinguisher_type in extinguisher_counts:
                    extinguisher_counts[extinguisher_type] += item.quantity
                else:
                    extinguisher_counts[extinguisher_type] = item.quantity
        return extinguisher_counts

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

    product_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    fire_class = models.CharField(max_length=20, choices=FIRE_CLASS_CHOICES)
    capacity = models.PositiveIntegerField()
    inspection_date = models.DateField()
    expiry_date = models.DateField()
    inventory = models.PositiveIntegerField()
    planned_sales = models.PositiveIntegerField()
    certification = models.CharField(max_length=50, choices=CERTIFICATION_CHOICES)
    standards_compliance = models.CharField(max_length=50, choices=STANDARDS_COMPLIANCE_CHOICES)
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    manufacture_date = models.DateField()
    warranty_period = models.PositiveIntegerField(help_text="Warranty period in months")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    companies = models.ManyToManyField(Company, related_name='fire_extinguishers')

    def __str__(self):
        return f"{self.name} ({self.type})"
    
    @staticmethod
    def projected_sales_for_year(year):
        # Get the start and end dates for the year
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        
        # Filter extinguishers expiring within the specified year
        expiring_extinguishers = FireExtinguisher.objects.filter(expiry_date__range=(start_date, end_date))
        
        # Sum up the total quantity of expiring extinguishers
        total_projected_sales = 0
        for extinguisher in expiring_extinguishers:
            # Assuming quantity is calculated from OrderItems
            quantity_sold = OrderItem.objects.filter(fire_extinguisher=extinguisher).aggregate(total=models.Sum('quantity'))['total']
            if quantity_sold:
                total_projected_sales += quantity_sold
        
        return total_projected_sales


# User Model
class User(models.Model):
    TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User')
    ]

    username = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Admin')
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.username

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

# ServiceSchedule Model
class ServiceSchedule(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='service_schedule')
    fire_extinguisher = models.ForeignKey(FireExtinguisher, on_delete=models.CASCADE, related_name='service_records')
    last_service_date = models.DateField()
    next_service_due = models.DateField()

    def __str__(self):
        return f"Service for {self.fire_extinguisher.name} - Next due: {self.next_service_due}"
