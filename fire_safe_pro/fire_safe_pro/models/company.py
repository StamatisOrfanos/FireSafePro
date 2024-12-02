from django.db import models


# Company Model
class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_calendar_events(self):
        all_events = []

        # Loop through each customer linked to the company
        for customer in self.customers.all():
            customer_events = customer.get_calendar_events()
            
            # Add each event with a reference to the customer
            for event in customer_events:
                event["customer_name"] = customer.name
                all_events.append(event)

        # Sort all events by date
        all_events.sort(key=lambda x: x["date"])
        return all_events