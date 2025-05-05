from django.db import models
from django.contrib.auth.models import User

class OTPStorage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    
# models.py
from django.db import models

class MilkProduction(models.Model):
    farmer_name = models.CharField(max_length=100)
    milk_quantity_liters = models.FloatField()
    procurement_date = models.DateField()
    plant_location = models.CharField(max_length=100)
    price_per_liter = models.FloatField()

    def __str__(self):
        return f"{self.farmer_name} - {self.milk_quantity_liters}L"

class NandiniShop(models.Model):
    shop_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    weekly_demand_liters = models.FloatField()

    def __str__(self):
        return self.shop_name
    
class Vehicle(models.Model):
    vehicle_id = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)
    capacity_liters = models.FloatField()
    driver_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default='Active')  # New field

    def __str__(self):
        return self.vehicle_id


class DeliverySchedule(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    shop = models.ForeignKey(NandiniShop, on_delete=models.CASCADE)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    route = models.TextField()

    def __str__(self):
        return f"Delivery to {self.shop.shop_name} on {self.delivery_date}"

class Order(models.Model):
    shop = models.ForeignKey(NandiniShop, on_delete=models.CASCADE)
    milk_quantity_liters = models.FloatField()
    order_date = models.DateField()
    delivery_date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Order for {self.milk_quantity_liters}L from {self.shop.shop_name}"

class QualityControl(models.Model):
    milk_batch_number = models.CharField(max_length=20)
    quality_check_date = models.DateField()
    quality_status = models.CharField(max_length=50)
    storage_facility = models.CharField(max_length=100)
    temperature = models.FloatField()

    def __str__(self):
        return f"Batch {self.milk_batch_number} - {self.quality_status}"

class MilkVariant(models.Model):
    variant_name = models.CharField(max_length=50)
    description = models.TextField(default='No description available')  # Set a default value here
    price_per_liter = models.FloatField()

    def __str__(self):
        return self.variant_name

class PricingStrategy(models.Model):
    variant = models.ForeignKey(MilkVariant, on_delete=models.CASCADE)
    region = models.CharField(max_length=100)
    subsidy = models.FloatField(default=0)

    def __str__(self):
        return f"Pricing for {self.variant.variant_name} in {self.region}"
