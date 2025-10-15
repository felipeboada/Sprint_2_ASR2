from django import forms
from .models import Measurement
from products.models import Variable

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = [
            'variable',
            'value',
            'unit',
            'place',
            #'dateTime',
        ]

        labels = {
            'variable' : 'Producto',
            'value' : 'Cantidad',
            'unit' : 'Unidad',
            'place' : 'Bodega',
            #'dateTime' : 'Date Time',
        }


class OrderForm(forms.Form):
    variable = forms.ModelChoiceField(queryset=Variable.objects.all(), label='Producto')
    units = forms.IntegerField(min_value=1, label='Cantidad')
