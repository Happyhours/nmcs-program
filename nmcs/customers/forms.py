from django import forms

from .models import Customer, Mc, Postal, Telephone, Model


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'street']
        widgets = { 
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if data:
            data = ''.join(data.split())
            data = data.strip()
            data = data.capitalize()

        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if data:
            data = ''.join(data.split())
            data = data.strip()
            data = data.capitalize()

        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if data:
            data = ''.join(data.split())
            data = data.strip()

        return data    

    def clean_street(self):
        data = self.cleaned_data['street']
        if data:
            data = data.strip()
            data = data.capitalize()

        return data


class McForm(forms.ModelForm):
    class Meta:
        model = Mc
        fields = ['registration_nr', 'year', 'motor', 'km']
        widgets = { 
            'registration_nr': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.TextInput(attrs={'class': 'form-control'}),
            'motor': forms.TextInput(attrs={'class': 'form-control'}),
            'km': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_registration_nr(self):
        data = self.cleaned_data['registration_nr']
        if data:
            data = ''.join(data.split())
            data = data.strip()
            data = data.upper()

        return data

    def clean_year(self):
        data = self.cleaned_data['year']
        if data:
            data = ''.join(data.split())
            data = data.strip()
            if not data.isnumeric():
                raise forms.ValidationError("Använd bara nummer.")

        return data

    def clean_motor(self):
        data = self.cleaned_data['motor']
        if data:
            data = data.strip()
            data = data.capitalize()   

        return data

    def clean_km(self):
        data = self.cleaned_data['km']
        if data:
            data = ''.join(data.split())
            data = data.strip()
            if not data.isnumeric():
                raise forms.ValidationError("Använd bara nummer.")

        return data


class PostalForm(forms.ModelForm):
    class Meta:
        model = Postal
        fields = ['postal', 'city']
        widgets = { 
            'postal': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_postal(self):
        data = self.cleaned_data['postal']
        print("cleanpostal")
        if data:
            data = ''.join(data.split())
            print("cleanpostal2: " + data)
            data = data.strip()
            if not data.isnumeric():
                print("invalid")
                raise forms.ValidationError("Använd ej bokstäver.")

        return data

    def clean_city(self):      
        data = self.cleaned_data['city']
        if data:
            data = ''.join(data.split())
            data = data.strip()
            data = data.capitalize()
            if not data.isalpha():
                raise forms.ValidationError("Använd ej nummer.")

        return data


class TelephoneForm(forms.ModelForm):
    class Meta:
        model = Telephone
        fields = ['number']
        widgets = { 
            'number': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_number(self):
        data = self.cleaned_data['number']
        if data:
            data = ''.join(data.split())
            data = data.strip()
            if not data.isnumeric():
                raise forms.ValidationError("Använd bara nummer.")

        return data


class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['model', 'brand']
        widgets = { 
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_model(self):      
        data = self.cleaned_data['model']
        if data:
            data = data.strip()
            data = data.upper()

            print(data)
        return data

    def clean_brand(self):
        data = self.cleaned_data['brand']
        if data:
            data = data.strip()
            data = data.title()

        return data


# Added this temporary to avoid modelform primary key error validation check.
class PostalFormNormal(forms.Form):
    postal = forms.CharField(max_length=50, widget = forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=50, widget = forms.TextInput(attrs={'class': 'form-control'}))

    def clean_postal(self):
        data = self.cleaned_data['postal']
        print("cleanpostal")
        if data:
            data = ''.join(data.split())
            print("cleanpostal2: " + data)
            data = data.strip()
            if not data.isnumeric():
                print("invalid")
                raise forms.ValidationError("Använd ej bokstäver.")

        return data

    def clean_city(self):      
        data = self.cleaned_data['city']
        if data:
            data = ''.join(data.split())
            data = data.strip()
            data = data.capitalize()
            if not data.isalpha():
                raise forms.ValidationError("Använd ej nummer.")

        return data


# Added this temporary to avoid modelform primary key error validation check.
class ModelFormNormal(forms.Form):
    model = forms.CharField(max_length=50, widget = forms.TextInput(attrs={'class': 'form-control'}))
    brand = forms.CharField(max_length=50, widget = forms.TextInput(attrs={'class': 'form-control'}))

    def clean_model(self):      
        data = self.cleaned_data['model']
        if data:
            data = data.strip()
            data = data.upper()

            print(data)
        return data

    def clean_brand(self):
        data = self.cleaned_data['brand']
        if data:
            data = data.strip()
            data = data.title()

        return data


class McFormNormal(forms.Form):
    registration_nr = forms.CharField(max_length=10, widget = forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.CharField(max_length=20, widget = forms.TextInput(attrs={'class': 'form-control'}))
    motor = forms.CharField(max_length=50, widget = forms.TextInput(attrs={'class': 'form-control'}))
    km = forms.CharField(max_length=20, widget = forms.TextInput(attrs={'class': 'form-control'}))

    def clean_registration_nr(self):
        data = self.cleaned_data['registration_nr']
        if data:
            data = ''.join(data.split())
            data = data.strip()
            data = data.upper()

        return data

    def clean_year(self):
        data = self.cleaned_data['year']
        if data:
            data = ''.join(data.split())
            data = data.strip()
            if not data.isnumeric():
                raise forms.ValidationError("Använd bara nummer.")

        return data

    def clean_motor(self):
        data = self.cleaned_data['motor']
        if data:
            data = data.strip()
            data = data.capitalize()   

        return data

    def clean_km(self):
        data = self.cleaned_data['km']
        if data:
            data = ''.join(data.split())
            data = data.strip()
            if not data.isnumeric():
                raise forms.ValidationError("Använd bara nummer.")

        return data

class ActiveMcForm(forms.Form):
    active_mc = forms.ModelChoiceField(queryset=Customer.objects.none(),
            required=True,
            empty_label=None,
            widget = forms.Select(attrs={'class': 'form-control', 'size': '5'})
    )

    def __init__(self, customer_pk, *args, **kwargs):
        super(ActiveMcForm, self).__init__(*args, **kwargs)
        customer = Customer.objects.get(pk=customer_pk)
        customer_mcs = customer.mc_set.all()
        self.fields['active_mc'].queryset=customer_mcs