from django import forms

from .models import Serviceprotocol

class ServiceprotocolForm(forms.ModelForm):
    class Meta:
        model = Serviceprotocol
        fields = [
            'model',
            'year',
            'km',
            'employee',
            'registration_nr', 
            'oil_check',
            'motor_check', 
            'primary_check', 
            'gearbox_check',
            'chain_check', 
            'cylinder_check',
            'brakes_check', 
            'front_check', 
            'back_check', 
            'plug_check',
            'rm_plug_check',
            'grease_check', 
            'air_check', 
            'rm_air_check', 
            'filter_check', 
            'belt_check', 
            'tires_check', 
            'pressure_check', 
            'fuel_check', 
            'layer_check', 
            'rm_layer_check', 
            'support_check', 
            'blinkers_check', 
            'error_check', 
            'additional', 
            'comment'
      
        ]

