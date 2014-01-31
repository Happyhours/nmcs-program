from django.db import models

# Create your models here.

class Postal(models.Model):
    postal = models.CharField(max_length=50, primary_key=True)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.postal


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    street = models.CharField(max_length=100)
    postal = models.ForeignKey(Postal)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['first_name']
        pass

class Telephone(models.Model):
    number = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer)

    def __str__(self):
        return self.number


class Model(models.Model):
    model = models.CharField(max_length=50, primary_key=True)
    brand = models.CharField(max_length=50)

    def __str__(self):
        return self.model


class Mc(models.Model):
    registration_nr = models.CharField(max_length=10, primary_key=True)
    active = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    year = models.CharField(max_length=20)
    motor = models.CharField(max_length=50)
    km = models.CharField(max_length=20)
    model = models.ForeignKey(Model)
    customer = models.ForeignKey(Customer)

    def __str__(self):
        return self.registration_nr















