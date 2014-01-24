from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory

# Create your views here.
from .models import Customer, Postal, Model
from .forms import CustomerForm, McForm, PostalForm, TelephoneForm, ModelForm

def helpPostal(postal, city):
    #Ta bort whitespaces från postal input
    postal = ''.join(postal.split())
    postal = postal.strip()
    #Lowercase pa city
    city = city.capitalize()

    return [postal, city]

def helpModel(model, brand):
    #Ta bort whitespaces från model input
    model = ''.join(model.split())
    model = model.strip()
    #Lowercase pa model
    model = model.capitalize()

    #Ta bort whitespaces från model input
    brand = ''.join(brand.split())
    brand = brand.strip()
    #Lowercase pa model
    brand = brand.capitalize()

    return [model, brand]   

def addView(request):

    #Formset for telephone
    #TelephoneFormSet = formset_factory(TelephoneForm, extra=2)


    if request.method == "POST":

        customer_form = CustomerForm(request.POST, prefix='customer')
        postal_form = PostalForm(request.POST, prefix='postal')
        #telephone_forms = TelephoneFormSet(request.POST, prefix='telephone')
        mc_form = McForm(request.POST, prefix='mc')
        model_form = ModelForm(request.POST, prefix='model')

        print(request.POST)
        if (request.POST['mc-registration_nr'] == '' and 
            request.POST['mc-year'] == '' and
            request.POST['mc-motor'] == '' and
            request.POST['mc-km'] == '' and
            request.POST['model-model'] == '' and 
            request.POST['model-brand'] == ''):

                if customer_form.is_valid() and postal_form.is_valid():

                    #Ta bort whitespaces från postal input
                    fixed = helpPostal(postal_form.cleaned_data['postal'],
                                postal_form.cleaned_data['city'])

                    #Kolla om postal finns redan
                    try: 
                        postal = Postal.objects.get(postal=fixed[0])
                        #postal_form = PostalForm(instance=postal)
                        print("Postal exists")
                    except Postal.DoesNotExist:
                        postal = postal_form.save(commit=False)
                        postal.postal = fixed[0]
                        postal.city = fixed[1]
                        postal.save()

                    customer = customer_form.save(commit=False)
                    customer.postal = postal
                    customer.save()


                    return HttpResponseRedirect('add')
        else:
            if mc_form.is_valid() and customer_form.is_valid() and postal_form.is_valid() and model_form.is_valid():

                #Ta bort whitespaces fran postal input
                postal_fixed = helpPostal(postal_form.cleaned_data['postal'],
                            postal_form.cleaned_data['city'])

                #Ta bort whitespaces fran postal input
                model_fixed = helpModel(model_form.cleaned_data['model'],
                            model_form.cleaned_data['brand'])
                
                #Kolla om postal finns redan
                try: 
                    postal = Postal.objects.get(postal=postal_fixed[0])
                    print("Postal exists")
                    #postal_form = PostalForm(instance=postal)
                except Postal.DoesNotExist:
                    postal = postal_form.save(commit=False)
                    postal.postal = postal_fixed[0]
                    postal.city = postal_fixed[1]
                    postal.save()

                #Kolla om model finns redan
                try: 
                    model = Model.objects.get(model=model_fixed[0])
                    print("Model exists")
                    #postal_form = PostalForm(instance=postal)
                except Model.DoesNotExist:
                    model = model_form.save(commit=False)
                    model.model = model_fixed[0]
                    model.brand = model_fixed[1]
                    model.save()


                customer = customer_form.save(commit=False)
                customer.postal = postal
                customer.save()

                mc = mc_form.save(commit=False)
                mc.active = True
                mc.customer = customer
                mc.model = model
                mc.save()

                return HttpResponseRedirect('add')

    else:
        customer_form = CustomerForm(prefix='customer')
        postal_form = PostalForm(prefix='postal')
        #telephone_forms = TelephoneFormSet(prefix='telephone')
        mc_form = McForm(prefix='mc')
        model_form = ModelForm(prefix='model')

    return render(request, 'customers/customer_add.html', 
        {'customer': customer_form, 'mc': mc_form, 'postal': postal_form,
        'model': model_form })


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
            # Return a filtered queryset
           return queryset.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(email__icontains=q) |
                Q(mc__registration_nr__icontains=q),
                mc__active=True
            )
        else:
            queryset = []
            return queryset
