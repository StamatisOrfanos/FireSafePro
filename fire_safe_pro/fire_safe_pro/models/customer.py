from django.db import models
import uuid
from datetime import date, timedelta
from .address import Address
from .company import Company


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
    
    
    def get_calendar_events(self):
        events = []

        # 1. Service Dates
        for service in self.service_schedule.all():
            service_event = {
                "type": "Service",
                "date": service.next_service_due,
                "customer_id": self.customer_id,
                "description": f"Service for {service.fire_extinguisher.name}"
            }
            reminder_date = service.next_service_due - timedelta(days=30)
            reminder_event = {
                "type": "Service Reminder",
                "date": reminder_date,
                "customer_id": self.customer_id,
                "description": f"Upcoming service reminder for {service.fire_extinguisher.name}"
            }
            events.extend([service_event, reminder_event])

        # 2. Inspection Dates
        for extinguisher in self.fire_extinguishers():
            inspection_event = {
                "type": "Inspection",
                "date": extinguisher.inspection_date,
                "customer_id": self.customer_id,
                "description": f"Inspection for {extinguisher.name}"
            }
            reminder_date = extinguisher.inspection_date - timedelta(days=30)
            reminder_event = {
                "type": "Inspection Reminder",
                "date": reminder_date,
                "customer_id": self.customer_id,
                "description": f"Upcoming inspection reminder for {extinguisher.name}"
            }
            events.extend([inspection_event, reminder_event])

        # 3. Expiry Dates
        for extinguisher in self.fire_extinguishers():
            expiry_event = {
                "type": "Expiry",
                "date": extinguisher.expiry_date,
                "customer_id": self.customer_id,
                "description": f"Expiry for {extinguisher.name}"
            }
            reminder_date = extinguisher.expiry_date - timedelta(days=30)
            reminder_event = {
                "type": "Expiry Reminder",
                "date": reminder_date,
                "customer_id": self.customer_id,
                "description": f"Upcoming expiry reminder for {extinguisher.name}"
            }
            events.extend([expiry_event, reminder_event])

        # Sort events by date
        events.sort(key=lambda x: x["date"])
        return events