from django.contrib import admin

from .models import Postal, Customer, Telephone, Model, Mc
# Register your models here.


admin.site.register(Postal)
admin.site.register(Customer)
admin.site.register(Telephone)
admin.site.register(Model)
admin.site.register(Mc)