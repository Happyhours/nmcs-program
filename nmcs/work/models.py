from django.db import models

from customers.models import Customer

import decimal

# Create your models here.

class Workorder(models.Model):
    job = models.TextField(blank=True)
    date = models.DateField(auto_now=True)
    notification = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    km = models.CharField(max_length=50)
    motor = models.CharField(max_length=50)
    registration_nr = models.CharField(max_length=50)

    customer = models.ForeignKey(Customer, null=True)


    def workorder_calculations(self):
        workorder = Workorder.objects.get(pk=self.pk)
        articles = workorder.article_set.all()

        cal = {}
        if articles:
            #Calculate the sum of all articles for this workorder
            summ = decimal.Decimal('0')
            for article in articles:
                total_price_of_articles = article.price * article.quantity
                print("Total: ",total_price_of_articles)
                summ += total_price_of_articles
            cal['sum'] = summ
            #Add and calculate from static values modified from Company app/model
            expendables = decimal.Decimal('0')
            cal['expendables'] = expendables
            vat_percentage = decimal.Decimal('1.20')
            cal['vat'] = (cal['sum']  * vat_percentage)
            cal['total'] = (cal['sum'] * vat_percentage) + expendables 
        else:
            #Default values if no articles
            cal['sum'] = decimal.Decimal('0')
            expendables = decimal.Decimal('0')
            cal['expendables'] = expendables
            vat_percentage = decimal.Decimal('0')
            cal['vat'] = (cal['sum'] * vat_percentage)
            cal['total'] = (cal['sum'] * vat_percentage) + expendables

        return cal

    # def update_active_mc(self, mc_object):
    #     # Get and Set active mc to false and save to db.
    #     current_active_mc = self.get_active_mc()
    #     current_active_mc.active = False
    #     current_active_mc.save()

    #     # Set selected mc to have active True and save to db.
    #     new_active_mc = mc_object
    #     new_active_mc.active = True
    #     new_active_mc.save()

    def __str__(self):
        return str(self.date)

class Article(models.Model):
    quantity = models.PositiveIntegerField()
    article_nr = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    price_total = models.DecimalField(null = True, max_digits=18, decimal_places=2)

    workorder = models.ForeignKey(Workorder)

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(self.article_nr.ljust(4,'_'), str(self.quantity).ljust(4,'_'), self.description[:15]+"...".ljust(4,'_'), str(self.price).ljust(4,'_'), 10000)
        #return "Artikel: {0} Antal: {1} {2} {3} {4}".format(self.article_nr.ljust(6,'#'), str(self.quantity).ljust(6,'#'), self.description[:15]+"...".rjust(6,'_'), str(self.price).rjust(6,'_'), str(10000).rjust(6,'_'))
        #return "Beskrivning: {0} ".format(self.description[:30]+"...")
        