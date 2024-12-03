from django.db import models
from datetime import date
from .company import Company



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
