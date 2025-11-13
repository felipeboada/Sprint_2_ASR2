import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


def validate_phone_number(value):
    if not value:
        return
    phone = re.sub(r'[\s\-\(\)]', '', str(value))
    if not re.match(r'^(\+57)?[36]\d{9}$|^(\+57)?[1-8]\d{6,7}$', phone):
        raise ValidationError('Número de teléfono inválido')


def validate_nit(value):
    if not value:
        return
    if not re.match(r'^\d{9}-\d$', str(value).strip()):
        raise ValidationError('NIT inválido. Formato: 123456789-0')


def validate_coordinates(latitude, longitude):
    if not (-4.5 <= latitude <= 13.5):
        raise ValidationError('Latitud fuera del rango válido para Colombia')
    if not (-79 <= longitude <= -66):
        raise ValidationError('Longitud fuera del rango válido para Colombia')


def validate_positive_quantity(value):
    if value is None or value <= 0:
        raise ValidationError('La cantidad debe ser mayor a cero')


def validate_non_negative(value):
    if value is None:
        raise ValidationError('Este campo es obligatorio')
    if value < 0:
        raise ValidationError('El valor no puede ser negativo')


def validate_name_format(value):
    if not value:
        raise ValidationError('El nombre es obligatorio')
    
    value = value.strip()
    if len(value) < 2 or len(value) > 100:
        raise ValidationError('El nombre debe tener entre 2 y 100 caracteres')
    
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
        raise ValidationError('El nombre solo puede contener letras y espacios')


def validate_address_format(value):
    if not value:
        return
    
    value = value.strip()
    if not (5 <= len(value) <= 200):
        raise ValidationError('La dirección debe tener entre 5 y 200 caracteres')
    
    if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s#\-,.°]+$', value):
        raise ValidationError('La dirección contiene caracteres no permitidos')


def validate_stock_availability(product, warehouse, requested_quantity):
    from orders.models import Inventory
    try:
        inventory = Inventory.objects.get(product=product, warehouse=warehouse)
        if inventory.quantity < requested_quantity:
            raise ValidationError(
                f'Stock insuficiente. Disponible: {inventory.quantity}, Solicitado: {requested_quantity}'
            )
    except Inventory.DoesNotExist:
        raise ValidationError('No hay inventario para este producto en la bodega seleccionada')


product_name_validator = RegexValidator(
    regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\-]+$',
    message='Nombre de producto inválido'
)

