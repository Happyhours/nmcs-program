from django.contrib import admin

from .models import Postal, Customer, Telephone
# Register your models here.


admin.site.register(Postal)
admin.site.register(Customer)
admin.site.register(Telephone)