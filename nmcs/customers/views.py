from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory

# Create your views here.
from .models import Customer, Postal, Model
from .forms import CustomerForm, McForm, PostalForm, TelephoneForm, ModelForm, PostalFormNormal, ModelFormNormal


def addView(request):

    #Formset for telephone
    TelephoneFormSet = formset_factory(TelephoneForm, extra=1)

    success = False

    if request.method == "POST":

        customer_form = CustomerForm(request.POST, prefix='customer')
        postal_form_normal = PostalFormNormal(request.POST, prefix='postal')
        telephone_forms = TelephoneFormSet(request.POST, prefix='telephone')
        telephone_form1 = TelephoneForm(request.POST, prefix='telephone1')
        mc_form = McForm(request.POST, prefix='mc')
        model_form_normal = ModelFormNormal(request.POST, prefix='model')



        model_form = ModelForm()
        postal_form = PostalForm()

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
                    mc_form = McForm(prefix='mc')
                    model_form_normal = ModelFormNormal(prefix='model')

        else:
            if mc_form.is_valid() and customer_form.is_valid() and postal_form_normal.is_valid() and model_form_normal.is_valid() and telephone_forms.is_valid() and telephone_form1.is_valid():

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

                mc = mc_form.save(commit=False)
                mc.active = True
                mc.customer = customer
                mc.model = model
                mc.save()

                return HttpResponseRedirect('add/?success=True')

    else:
        if request.GET.get('success'):
            success = True

        customer_form = CustomerForm(prefix='customer')
        postal_form_normal = PostalFormNormal(prefix='postal')
        telephone_form1 = TelephoneForm(prefix='telephone1')
        telephone_forms = TelephoneFormSet(prefix='telephone')
        mc_form = McForm(prefix='mc')
        model_form_normal = ModelFormNormal(prefix='model')

    return render(request, 'customers/customer_add.html', 
        {'customer': customer_form, 'mc': mc_form, 'postal': postal_form_normal,
        'model': model_form_normal, 'telephones': telephone_forms, 'telephone1': telephone_form1, 'success': success })


class CustomerDetailView(generic.DetailView):
    model = Customer
    context_object_name = 'customer_detail'
    template_name = 'customers/customer_detail.html'


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
            return queryset.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(email__icontains=q) |
                Q(mc__registration_nr__icontains=q)
            )
        else:
            # Set attribute search to False to indicate no custom search
            self.search = False
            return queryset

    def get_context_data(self, **kwargs):
        context = super(CustomerListView, self).get_context_data(**kwargs)
        # Add boolean search atrribute from get_queryset() to context
        context['search'] = self.search

        return context
