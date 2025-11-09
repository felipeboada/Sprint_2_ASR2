from django.shortcuts import render
from .forms import MeasurementForm, OrderForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .logic.logic_measurement import create_measurement, get_measurements
from orders.logic import place_order_atomic


def measurement_list(request):
    inventories = get_measurements()
    context = {
        'inventories': inventories
    }
    return render(request, 'Inventory/measurements.html', context)


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


def measurement_order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            variable = form.cleaned_data['variable']
            units = form.cleaned_data['units']
            order, confirmed = place_order_atomic(variable.name, units)
            if confirmed:
                messages.add_message(request, messages.SUCCESS, 'Order placed successfully')
            else:
                messages.add_message(request, messages.ERROR, 'Order rejected due to insufficient stock')
            return HttpResponseRedirect(reverse('orderCreate'))
        else:
            print(form.errors)
    else:
        form = OrderForm()

    context = {
        'form': form,
    }

    return render(request, 'Inventory/measurementOrderCreate.html', context)