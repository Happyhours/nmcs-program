from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView, DetailView

# Create your views here.

from .models import (
    Serviceprotocol 
)

from .forms import ( 
    ServiceprotocolForm
)

from customers.models import Customer

#class ServiceCreateView(CreateView):

def TestCreateView(request, *args, **kwargs):
    return render(request, 'service/service_create.html', {})


class ServiceCreateView(CreateView):
    model = Serviceprotocol
    form_class = ServiceprotocolForm
    template_name = 'service/service_create.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        self.object = None

        customer = Customer.objects.get(pk=self.kwargs.get(self.pk_url_kwarg, None))
        mc = customer.get_active_mc()
        self.initial = {'model': mc.model.model,
                        'year': mc.year,
                        'km': mc.km}

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form, reg=mc.registration_nr))

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        return reverse('customer-detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(ServiceCreateView, self).get_context_data(**kwargs)
        # Add boolean search atrribute from get_queryset() to context
        context['pk'] = self.kwargs.get(self.pk_url_kwarg, None)

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        customer = Customer.objects.get(pk=self.kwargs.get(self.pk_url_kwarg, None))
        #Fetch motorcykle
        mc = customer.get_active_mc()
        self.object.registration_nr = mc.registration_nr
        self.object.customer = customer
        self.object.save()

        #Also modify the real motorcykle and not only the form temporary values!
        mc.model.model = self.object.model
        mc.year = self.object.year
        mc.km = self.object.km
        mc.save()

        

        return HttpResponseRedirect(self.get_success_url())


class ServiceUpdateView(UpdateView):
    model = Serviceprotocol
    form_class = ServiceprotocolForm
    template_name = 'service/service_update.html'

    def get_success_url(self):
        return reverse('service-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ServiceUpdateView, self).get_context_data(**kwargs)
        # Add boolean search atrribute from get_queryset() to context
        context['pk'] = self.object.pk

        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        #check if form has been modifed
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class ServiceDetailView(DetailView):
    model = Serviceprotocol
    template_name = 'service/service_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(**kwargs)
        # Add boolean search atrribute from get_queryset() to context
        context['pk'] = self.object.pk

        return context




class ServiceDeleteView(DeleteView):
    model = Serviceprotocol
    template_name = 'service/service_confirm_delete.html'


    def get_success_url(self):
        return reverse('customer-detail', kwargs={'pk': self.object.customer.pk})


