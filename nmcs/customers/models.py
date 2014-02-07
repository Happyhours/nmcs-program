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

    def get_active_mc(self):
        customer = Customer.objects.get(pk=self.pk)
        try:
            return customer.mc_set.get(active=True)
        except Mc.DoesNotExist:
            print("No active mc exists for this customer")
            return []

    def update_active_mc(self, mc_object):
        # Get and Set active mc to false and save to db.
        current_active_mc = self.get_active_mc()
        current_active_mc.active = False
        current_active_mc.save()

        # Set selected mc to have active True and save to db.
        new_active_mc = mc_object
        new_active_mc.active = True
        new_active_mc.save()

    def set_removed_on_mcs(self):
        customer = Customer.objects.get(pk=self.pk)
        mcs = customer.mc_set.all()
        if mcs:
            for mc in mcs:
                mc.removed = True
                mc.active = False
                mc.save()


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
    customer = models.ForeignKey(Customer,null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.registration_nr
















