from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory
from django.core.urlresolvers import reverse

from django.forms.models import inlineformset_factory
from django import forms

# Create your views here.
from .models import (
    Customer,
    Postal,
    Model,
    Mc, 
    Telephone
)

from .forms import ( 
    CustomerForm, 
    McForm, 
    PostalForm, 
    TelephoneForm, 
    ModelForm, 
    PostalFormNormal, 
    ModelFormNormal, 
    ActiveMcForm, 
    McFormNormal,
    telephoneInlineFormset,
    mcInlineFormset,
    McFormUpdate

)


def addView(request, *args, **kwargs):

    #Formset for telephone
    TelephoneFormSet = formset_factory(TelephoneForm, extra=1)

    success = False

    if request.method == "POST":
        print(request.POST)
        customer_form = CustomerForm(request.POST, prefix='customer')
        postal_form_normal = PostalFormNormal(request.POST, prefix='postal')
        telephone_forms = TelephoneFormSet(request.POST, prefix='telephone')
        telephone_form1 = TelephoneForm(request.POST, prefix='telephone1')
        mc_form_normal = McFormNormal(request.POST, prefix='mc')
        model_form_normal = ModelFormNormal(request.POST, prefix='model')

        model_form = ModelForm()
        postal_form = PostalForm()
        mc_form = McForm()

        # print(request.POST)
        if (request.POST['mc-registration_nr'] == '' and 
            request.POST['mc-year'] == '' and
            request.POST['mc-motor'] == '' and
            request.POST['mc-km'] == '' and
            request.POST['model-model'] == '' and 
            request.POST['model-brand'] == ''):

                if customer_form.is_valid() and postal_form_normal.is_valid() and telephone_forms.is_valid() and telephone_form1.is_valid():

                    try: 
                        postal = Postal.objects.get(postal=postal_form_normal.cleaned_data['postal'])
                    except Postal.DoesNotExist:
                        postal = postal_form.save(commit=False)
                        postal.postal = postal_form_normal.cleaned_data['postal']
                        postal.city = postal_form_normal.cleaned_data['city']
                        postal.save()

                    customer = customer_form.save(commit=False)
                    customer.postal = postal
                    customer.save()

                    telephone1 = telephone_form1.save(commit=False)
                    telephone1.number = telephone_form1.cleaned_data['number']
                    telephone1.customer = customer
                    telephone1.save()

                    for telephones in telephone_forms:
                        if not telephones.cleaned_data == {}:   
                            telephone = telephones.save(commit=False)
                            telephone.number = telephones.cleaned_data['number']
                            telephone.customer = customer
                            telephone.save()

                    return HttpResponseRedirect('add/?success=True')
                else:
                    mc_form_normal = McFormNormal(prefix='mc')
                    model_form_normal = ModelFormNormal(prefix='model')

        else:
            if mc_form_normal.is_valid() and customer_form.is_valid() and postal_form_normal.is_valid() and model_form_normal.is_valid() and telephone_forms.is_valid() and telephone_form1.is_valid():

                try: 
                    postal = Postal.objects.get(postal=postal_form_normal.cleaned_data['postal'])
                except Postal.DoesNotExist:
                    postal = postal_form.save(commit=False)
                    postal.postal = postal_form_normal.cleaned_data['postal']
                    postal.city = postal_form_normal.cleaned_data['city']
                    postal.save()

                try: 
                    model = Model.objects.get(model=model_form_normal.cleaned_data['model'])
                except Model.DoesNotExist:
                    model = model_form.save(commit=False)
                    model.model = model_form_normal.cleaned_data['model']
                    model.brand = model_form_normal.cleaned_data['brand']
                    model.save()

                customer = customer_form.save(commit=False)
                customer.postal = postal
                customer.save()

                try: 
                    mc = Mc.objects.get(registration_nr=mc_form_normal.cleaned_data['registration_nr'])
                    mc.removed = False
                    mc.active = True
                    mc.customer = customer
                    mc.save()
                except Mc.DoesNotExist:
                    mc = mc_form.save(commit=False)
                    mc.registration_nr = mc_form_normal.cleaned_data['registration_nr']
                    mc.year = mc_form_normal.cleaned_data['year']
                    mc.motor = mc_form_normal.cleaned_data['motor']
                    mc.km = mc_form_normal.cleaned_data['km']
                    mc.active = True
                    mc.removed = False
                    mc.customer = customer
                    mc.model = model
                    mc.save()

                telephone1 = telephone_form1.save(commit=False)
                telephone1.number = telephone_form1.cleaned_data['number']
                telephone1.customer = customer
                telephone1.save()

                for telephones in telephone_forms:
                    if not telephones.cleaned_data == {}:   
                        telephone = telephones.save(commit=False)
                        telephone.number = telephones.cleaned_data['number']
                        telephone.customer = customer
                        telephone.save()

                return HttpResponseRedirect('add/?success=True')

    else:
        if request.GET.get('success'):
            success = True

        customer_form = CustomerForm(prefix='customer')
        postal_form_normal = PostalFormNormal(prefix='postal')
        telephone_form1 = TelephoneForm(prefix='telephone1')
        telephone_forms = TelephoneFormSet(prefix='telephone')
        mc_form_normal = McFormNormal(prefix='mc')
        model_form_normal = ModelFormNormal(prefix='model')

    return render(request, 'customers/customer_add.html', 
        {'customer': customer_form, 'mc': mc_form_normal, 'postal': postal_form_normal,
        'model': model_form_normal, 'telephones': telephone_forms, 'telephone1': telephone_form1, 'success': success })


class CustomerListView(generic.ListView):
    model = Customer
    context_object_name = 'customer_list'
    template_name = 'customers/customer_list.html'

    def get_queryset(self):
        # Fetch queryset from the parent(ListView) get_queryset.
        queryset = super(CustomerListView, self).get_queryset()

        # Get the q GET parameter
        q = self.request.GET.get("q")
        if q:
            # Set attribute search to indicate custom search
            self.search = True
            # Return a filtered queryset
            # eg (A OR B OR C) OR (D AND E)
            return queryset.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(email__icontains=q) |
                Q(mc__registration_nr__icontains=q)
            ).distinct()
        else:
            # Set attribute search to False to indicate no custom search
            self.search = False
            return queryset

    def get_context_data(self, **kwargs):
        context = super(CustomerListView, self).get_context_data(**kwargs)
        # Add boolean search atrribute from get_queryset() to context
        context['search'] = self.search

        return context


class CustomerDetailView(generic.detail.DetailView):
    model = Customer
    context_object_name = 'customer_detail'
    template_name = 'customers/customer_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)

        #Fetch serviceprotocols and add to context
        context['serviceprotocols'] = self.get_object().serviceprotocol_set.all()

        # Check if customer has a mc
        if self.get_object().mc_set.all().filter(active=True):
            #context['mc_form'] = ActiveMcForm(self.object.pk, initial = {'active_mc': self.object.mc_set.get(active=True)}, prefix="active_mc")
            initial = {'active_mc': self.object.mc_set.get(active=True)}
            context['mc_form'] = ActiveMcForm(customer_pk=self.object.pk, initial = {'active_mc': self.object.mc_set.get(active=True)})
            context['mc'] = self.object.mc_set.get(active=True)
        else:
            context['mc_form'] = []
            context['mc'] = []

        return context


class CustomerFormView(generic.detail.SingleObjectMixin, generic.edit.FormView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    form_class = ActiveMcForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CustomerFormView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwarg = super(CustomerFormView, self).get_form_kwargs()
        kwarg['customer_pk']=self.object.pk
        return kwarg

    def form_valid(self, form):
        # Updates the selected mc as the new active mc.
        self.object.update_active_mc(form.cleaned_data['active_mc'])
        return super(CustomerFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('customer-detail', kwargs={'pk': self.object.pk})


class CustomerView(generic.base.View):

    def get(self, request, *args, **kwargs):
        view = CustomerDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CustomerFormView.as_view()
        return view(request, *args, **kwargs)


class CustomerDeleteView(generic.edit.DeleteView):
    model = Customer
    context_object_name = 'customer_delete'

    def delete(self, request, *args, **kwargs):
        # Set all motorcykles Removed flag to True.
        self.object = self.get_object()
        self.object.set_removed_on_mcs()
        return super(CustomerDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('customer-list')


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm # instance=Customer
    template_name = 'customers/customer_update.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        telephone_formset = telephoneInlineFormset(instance=self.object)
        postal_form = PostalFormNormal(initial={'postal': self.object.postal, 'city': self.object.postal.city})

        return self.render_to_response(self.get_context_data(form=form,
                                       telephone_formset=telephone_formset,
                                       postal_form=postal_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        telephone_formset = telephoneInlineFormset(self.request.POST, instance=self.object)
        postal_form = PostalFormNormal(self.request.POST)

        if form.is_valid() and telephone_formset.is_valid() and postal_form.is_valid():
            return self.form_valid(form, telephone_formset, postal_form)
        else:
            return self.form_invalid(form, telephone_formset, postal_form)

    def form_valid(self, form, telephone_formset, postal_form):

        try: 
            postal = Postal.objects.get(postal=postal_form.cleaned_data['postal'])
        except Postal.DoesNotExist:
            postal = Postal.objects.create(postal=postal_form.cleaned_data['postal'], 
                                      city=postal_form.cleaned_data['city'])

        self.object.postal = postal
        self.object.save()
        telephone_formset.save()

        return super(CustomerUpdateView, self).form_valid(form)

    def form_invalid(self, form, telephone_formset, postal_form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(self.get_context_data(form=form,
                                       telephone_formset=telephone_formset,
                                       postal_form=postal_form))

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('customer-detail', kwargs={'pk': self.object.pk})


class McUpdateView(UpdateView):
    model = Mc
    template_name = 'customers/mc_update.html'
    form_class = McFormUpdate
    
    def get(self,request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        self.object = self.get_object()

        model_form = ModelFormNormal(initial={'model': self.object.model, 'brand': self.object.model.brand})

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form, model_form=model_form))     


    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.object = self.get_object()

        model_form = ModelFormNormal(self.request.POST)

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid() and model_form.is_valid():
            return self.form_valid(form, model_form)
        else:
            return self.form_invalid(form, model_form)

    def form_valid(self, form, model_form):

        try: 
            model = Model.objects.get(model=model_form.cleaned_data['model'])
        except Model.DoesNotExist:
            model = Model.objects.create(model=model_form.cleaned_data['model'], 
                                         brand=model_form.cleaned_data['brand'])

        self.object.model = model
        self.object.save()

        return super(McUpdateView, self).form_valid(form)

    def form_invalid(self, form, model_form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(self.get_context_data(form=form, model_formset=model_formset))

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('customer-detail', kwargs={'pk': self.object.customer.pk})


class McDeleteView(DeleteView):
    model = Mc
    template_name = 'customers/mc_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()

        customer = self.object.customer
        listan = customer.mc_set.filter(active=False, removed=False)
        if listan.count() >= 1:
            new_active_mc = listan[0]
            new_active_mc.active = True       
            new_active_mc.save()  

        self.object.active = False
        self.object.removed = True
        self.object.customer = None
        self.object.save()


        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('customer-detail', kwargs={'pk': self.object.customer.pk})
            

class McCreateView(CreateView):
    model = Customer
    form_class = McFormNormal
    template_name = 'customers/mc_form.html'

    def get_success_url(self):
        return reverse('customer-detail', kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        self.object = self.get_object()
        model_form = ModelFormNormal()
        form = self.form_class()

        return self.render_to_response(self.get_context_data(form=form, model_form=model_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.object = self.get_object()

        model_form = ModelFormNormal(self.request.POST)
        form = self.form_class(self.request.POST)

        if form.is_valid() and model_form.is_valid():
            return self.form_valid(form, model_form)
        else:
            return self.form_invalid(form, model_form)

    def form_valid(self, form, model_form):

        try: 
            model = Model.objects.get(model=model_form.cleaned_data['model'])
        except Model.DoesNotExist:
            model = Model.objects.create(model=model_form.cleaned_data['model'], 
                                         brand=model_form.cleaned_data['brand'])

        try: 
            mc = Mc.objects.get(registration_nr=form.cleaned_data['registration_nr'])
            mc.removed = False
            if self.object.get_active_mc() == []:
                mc.active = True
            else:
                mc.active = False
            mc.customer = self.object
            mc.model = model
            mc.save()
        except Mc.DoesNotExist:
            mc = Mc()
            mc.registration_nr = form.cleaned_data['registration_nr']
            mc.year = form.cleaned_data['year']
            mc.motor = form.cleaned_data['motor']
            mc.km = form.cleaned_data['km']
            if self.object.get_active_mc() == []:
                mc.active = True
            else:
                mc.active = False
            mc.removed = False
            mc.customer = self.object
            mc.model = model
            mc.save()


        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, model_form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(self.get_context_data(form=form, model_form=model_form))




