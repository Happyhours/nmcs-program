from django.shortcuts import render
from django.views import generic

# Create your views here.
from .models import Postal, Customer, Telephone

class CustomerDetailView(generic.DetailView):
    model = Customer
    context_object_name = 'customer'
    template_name = 'customers/customer_detail.html'


#def index(request):
#    return HttpResponse("Hello world you are at index page")