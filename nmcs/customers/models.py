from django.db import models

# Create your models here.

def Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    street = models.CharField(max_length=100)
    postal = models.ForeignKey(Postal)

    def __str__(self):
        return self.first_name


def Telephone(models.Model):
    number = CharField(max_length=50)
    customer = models.ForeignKey(Customer)

    def __str__(self):
        return self.number


def Postal(models.Model):
    postal = models.CharField(max_length=50, primary_key=True)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.postal


