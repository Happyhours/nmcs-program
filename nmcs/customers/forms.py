from django import forms

from .models import Customer, Mc, Postal, Telephone, Model

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'street']


class McForm(forms.ModelForm):
    class Meta:
        model = Mc
        fields = ['registration_nr', 'year', 'motor', 'km']

class PostalForm(forms.ModelForm):
    class Meta:
        model = Postal
        fields = ['postal', 'city']

class TelephoneForm(forms.ModelForm):
    class Meta:
        model = Telephone
        fields = ['number']

class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['model', 'brand']