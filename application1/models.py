from django.db import models


class login(models.Model):

    username = models.CharField(max_length=30)

    mobilenumber = models.CharField(max_length=15)

    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username


# CATEGORY MODEL FIRST
class Category(models.Model):

    area_number = models.CharField(max_length=100)

    vehicle_type = models.CharField(max_length=100)

    vehicle_limit = models.IntegerField()

    parking_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.BooleanField(default=True)

    def __str__(self):
        return self.vehicle_type


# VEHICLE ENTRY MODEL
class VehicleEntry(models.Model):

    STATUS_CHOICES = [
        ('Parked', 'Parked'),
        ('Leaved', 'Leaved'),
    ]

    ACTION_CHOICES = [
        ('Parked', 'Parked'),
        ('Leaved', 'Leaved'),
    ]

    vehicle_number = models.CharField(max_length=20)

    vehicle_type = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    area_no = models.CharField(max_length=100)

    charge = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    arrival_time = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Parked'
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        default='register'
    )

    def __str__(self):
        return self.vehicle_number
class SubCategory(models.Model):

    category = models.CharField(
    max_length=100,
    null=True,
    blank=True
)

    vehicle_type = models.CharField(max_length=100)

    area_number = models.CharField(max_length=100)

    parking_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.BooleanField(default=True)

    def __str__(self):
        return self.vehicle_type