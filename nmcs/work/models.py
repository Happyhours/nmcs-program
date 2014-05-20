from django.db import models

from customers.models import Customer

# Create your models here.

class Workorder(models.Model):
    job = models.TextField(blank=True)
    date = models.DateField(auto_now=True)
    notification = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    model = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    km = models.CharField(max_length=50)
    motor = models.CharField(max_length=50)
    registration_nr = models.CharField(max_length=50)

    customer = models.ForeignKey(Customer, null=True)

    def __str__(self):
        return str(self.date)

class Article(models.Model):
    quantity = models.PositiveIntegerField()
    article_nr = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()

    workorder = models.ForeignKey(Workorder)

    def __str__(self):
        return self.article_nr