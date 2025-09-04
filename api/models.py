from django.db import models


# Model representing an order
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    pickup_addr = models.CharField(max_length=100)
    delivery_addr = models.CharField(max_length=100)
    total_weight = models.FloatField()
    date = models.DateField()
    status = models.BooleanField()  # True = processed, False = not processed

    def __str__(self):
        return self.customer_name


# Model representing a vehicle
class Vehicles(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    license_plate = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)
    max_capacity = models.FloatField()
    cost_per_km = models.FloatField()
    current_position = models.CharField(max_length=100)  # town name, must match JSON keys
    availability_status_vehicle = models.BooleanField()

    def __str__(self):
        return self.license_plate


# Model representing a driver
class Drivers(models.Model):
    driver_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    availability_status_driver = models.BooleanField()

    def __str__(self):
        return self.name
