from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView

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
                        'km': mc.km,
                        'employee': 'TESTPERSON',
                        'registration_nr': mc.registration_nr}

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

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
        self.object.customer = customer
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

class ServiceUpdateView(UpdateView):
    model = Serviceprotocol
    form_class = ServiceprotocolForm
    template_name = 'service/service_update.html'

# class McCreateView(CreateView):
#     model = Customer
#     form_class = McFormNormal
#     template_name = 'customers/mc_form.html'

#     def get_success_url(self):
#         return reverse('customer-detail', kwargs={'pk': self.object.pk})

#     def get(self, request, *args, **kwargs):
#         """
#         Handles GET requests and instantiates a blank version of the form.
#         """
#         self.object = self.get_object()
#         model_form = ModelFormNormal()
#         form = self.form_class()

#         return self.render_to_response(self.get_context_data(form=form, model_form=model_form))

#     def post(self, request, *args, **kwargs):
#         """
#         Handles POST requests, instantiating a form instance with the passed
#         POST variables and then checked for validity.
#         """
#         self.object = self.get_object()

#         model_form = ModelFormNormal(self.request.POST)
#         form = self.form_class(self.request.POST)

#         if form.is_valid() and model_form.is_valid():
#             return self.form_valid(form, model_form)
#         else:
#             return self.form_invalid(form, model_form)

#     def form_valid(self, form, model_form):

#         try: 
#             model = Model.objects.get(model=model_form.cleaned_data['model'])
#         except Model.DoesNotExist:
#             model = Model.objects.create(model=model_form.cleaned_data['model'], 
#                                          brand=model_form.cleaned_data['brand'])

#         try: 
#             mc = Mc.objects.get(registration_nr=form.cleaned_data['registration_nr'])
#             mc.removed = False
#             if self.object.get_active_mc() == []:
#                 mc.active = True
#             else:
#                 mc.active = False
#             mc.customer = self.object
#             mc.model = model
#             mc.save()
#         except Mc.DoesNotExist:
#             mc = Mc()
#             mc.registration_nr = form.cleaned_data['registration_nr']
#             mc.year = form.cleaned_data['year']
#             mc.motor = form.cleaned_data['motor']
#             mc.km = form.cleaned_data['km']
#             if self.object.get_active_mc() == []:
#                 mc.active = True
#             else:
#                 mc.active = False
#             mc.removed = False
#             mc.customer = self.object
#             mc.model = model
#             mc.save()


#         return HttpResponseRedirect(self.get_success_url())

#     def form_invalid(self, form, model_form):
#         """
#         If the form is invalid, re-render the context data with the
#         data-filled form and errors.
#         """
#         return self.render_to_response(self.get_context_data(form=form, model_form=model_form))


