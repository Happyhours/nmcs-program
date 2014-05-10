from django.db import models

from customers.models import Customer

# Create your models here.

class Serviceprotocol(models.Model):
    date = models.DateField(auto_now=True)
    oil_check = models.BooleanField()
    motor_check = models.BooleanField()
    primary_check = models.BooleanField()
    gearbox_check = models.BooleanField()
    chain_check = models.BooleanField()
    cylinder_check = models.BooleanField()
    brakes_check = models.BooleanField()
    front_check = models.BooleanField()
    back_check = models.BooleanField()
    plug_check = models.BooleanField()
    rm_plug_check = models.BooleanField()
    grease_check = models.BooleanField()
    air_check = models.BooleanField()
    rm_air_check = models.BooleanField()
    filter_check = models.BooleanField()
    belt_check = models.BooleanField()
    tires_check = models.BooleanField()
    pressure_check = models.BooleanField()
    fuel_check = models.BooleanField()
    layer_check = models.BooleanField()
    rm_layer_check = models.BooleanField()
    support_check = models.BooleanField()
    blinkers_check = models.BooleanField()
    error_check = models.BooleanField()
    additional = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    model = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    km = models.CharField(max_length=50)
    employee = models.CharField(max_length=50,blank=True)
    registration_nr = models.CharField(max_length=50)

    customer = models.ForeignKey(Customer)



    def __str__(self):
        return self.employee