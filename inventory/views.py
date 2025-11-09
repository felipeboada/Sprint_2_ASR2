from django.shortcuts import render
from .forms import MeasurementForm, OrderForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .logic.logic_measurement import create_measurement, get_measurements
from orders.logic import place_order_atomic
from authentication.decorators import operario_required, cliente_required


@operario_required
def measurement_list(request):
    inventories = get_measurements()
    context = {
        'inventories': inventories
    }
    return render(request, 'Inventory/measurements.html', context)


@operario_required
def measurement_create(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            create_measurement(form)
            messages.add_message(request, messages.SUCCESS, 'Stock restocked successfully')
            return HttpResponseRedirect(reverse('stockCreate'))
        else:
            print(form.errors)
    else:
        form = MeasurementForm()

    context = {
        'form': form,
    }

    return render(request, 'Inventory/measurementCreate.html', context)


@cliente_required
def measurement_order_create(request):
    # Mapa de zonas de entrega a coordenadas (Bogotá)
    ZONE_COORDINATES = {
        'norte': (4.710989, -74.072092),      # Usaquén
        'centro': (4.598889, -74.080833),     # Teusaquillo
        'sur': (4.570868, -74.297333),        # Kennedy
        'occidente': (4.680389, -74.146667),  # Fontibón
        'oriente': (4.567778, -74.086111),    # San Cristóbal
    }
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            variable = form.cleaned_data['variable']
            units = form.cleaned_data['units']
            delivery_zone = form.cleaned_data['delivery_zone']
            
            # Obtener coordenadas de la zona seleccionada
            latitude, longitude = ZONE_COORDINATES.get(delivery_zone, (4.598889, -74.080833))
            
            try:
                # Intentar crear el pedido con ubicación del usuario
                order, confirmed = place_order_atomic(
                    product_name=variable.name,
                    units=units,
                    user_lat=latitude,
                    user_lon=longitude
                )
                
                if confirmed:
                    warehouse_name = order.assigned_warehouse.name if order.assigned_warehouse else "N/A"
                    zone_display = dict(form.fields['delivery_zone'].choices).get(delivery_zone, delivery_zone)
                    messages.success(
                        request, 
                        f'✓ Pedido #{order.id} confirmado exitosamente! '
                        f'Producto: {variable.name}, Cantidad: {units} unidades. '
                        f'Zona de entrega: {zone_display}. '
                        f'Se despachará desde: {warehouse_name}'
                    )
                else:
                    messages.error(
                        request, 
                        f'✗ Pedido rechazado: No hay suficiente stock disponible de "{variable.name}". '
                        f'Solicitaste {units} unidades pero no hay inventario disponible en ninguna bodega cercana.'
                    )
            except Exception as e:
                messages.error(
                    request,
                    f'✗ Error al procesar el pedido: {str(e)}'
                )
            
            return HttpResponseRedirect(reverse('orderCreate'))
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
    else:
        form = OrderForm()

    context = {
        'form': form,
    }

    return render(request, 'Inventory/measurementOrderCreate.html', context)