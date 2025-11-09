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
    # Zonas de entrega predefinidas con sus coordenadas
    DELIVERY_ZONES = [
        ('norte', 'Zona Norte - Usaquén, Chapinero, Suba'),
        ('centro', 'Zona Centro - Teusaquillo, Santa Fe, Candelaria'),
        ('sur', 'Zona Sur - Kennedy, Bosa, Tunjuelito'),
        ('occidente', 'Zona Occidente - Fontibón, Engativá'),
        ('oriente', 'Zona Oriente - San Cristóbal, Usme'),
    ]
    
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.all(), 
        label='Producto',
        help_text='Selecciona el producto que deseas ordenar'
    )
    units = forms.IntegerField(
        min_value=1, 
        label='Cantidad',
        help_text='Número de unidades a solicitar'
    )
    delivery_zone = forms.ChoiceField(
        choices=DELIVERY_ZONES,
        label='Zona de Entrega',
        initial='centro',
        help_text='Selecciona la zona donde deseas recibir tu pedido'
    )
