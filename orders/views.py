# orders/views.py
import json, time
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .logic import get_inventory, restock_atomic, place_order_atomic
from .serializers import InventorySerializer, OrderSerializer


@require_http_methods(["GET"])
def inventory_detail(request, product_name: str):

    qs = get_inventory(product_name)

    data = InventorySerializer(qs, many=True).data

    return JsonResponse(data, safe=False, status=200)


@require_http_methods(["POST"])
def inventory_restock(request, product_name: str):

    try:
        payload = json.loads(request.body.decode("utf-8")) if request.body else {}
        units = int(payload.get("units", 0))
        warehouse = payload["warehouse"]
    except (KeyError, ValueError, json.JSONDecodeError):
        return HttpResponseBadRequest('Payload: {"units":int,"warehouse":"Nombre"}')
    
    inv = restock_atomic(product_name, units, warehouse)
    from .serializers import InventorySerializer
    return JsonResponse(InventorySerializer(inv).data, status=200)


@require_http_methods(["POST"])
def place_order(request, product_name: str):

    try:
        payload = json.loads(request.body.decode("utf-8")) if request.body else {}
        units = int(payload.get("units", 0))
        user_lat = float(payload["lat"]); user_lon = float(payload["lon"])
        main_warehouse_name = payload.get("mainWarehouse")
    except (KeyError, ValueError, json.JSONDecodeError):
        return HttpResponseBadRequest('Payload: {"units":int,"lat":float,"lon":float,"mainWarehouse"?:str}')
    order, confirmed = place_order_atomic(product_name, units, user_lat, user_lon, main_warehouse_name)

    data = OrderSerializer(order).data
    
    return JsonResponse({"order": data, "confirmed": confirmed}, status=200 if confirmed else 409)


@csrf_exempt
@require_http_methods(["POST"])
def create_order_view(request):
    """
    Crea una orden automática verificando disponibilidad en todas las bodegas.
    Asigna la más cercana con stock y actualiza el estado.
    Cumple con el ASR: ejecución < 5s y reasignación inteligente.
    """

    start_time = time.time()

    try:
        payload = json.loads(request.body.decode("utf-8")) if request.body else {}
        product_name = payload["product"]
        units = int(payload["units"])
        user_lat = float(payload["lat"])
        user_lon = float(payload["lon"])
        main_warehouse_name = payload.get("mainWarehouse")
    except (KeyError, ValueError, json.JSONDecodeError):
        return HttpResponseBadRequest(
            'Payload inválido. Ejemplo: {"product": "Monitor LED 24\"", "units": 5, "lat": 4.6, "lon": -74.08, "mainWarehouse": "Bodega Sur"}'
        )

    order, confirmed = place_order_atomic(
        product_name=product_name,
        units=units,
        user_lat=user_lat,
        user_lon=user_lon,
        main_warehouse_name=main_warehouse_name
    )

    elapsed = round(time.time() - start_time, 3)

    return JsonResponse({
        "order_id": order.id,
        "product": order.product.name,
        "units": order.units,
        "status": order.status,
        "assigned_warehouse": order.assigned_warehouse.name if order.assigned_warehouse else None,
        "confirmed": confirmed,
        "execution_time_seconds": elapsed,
        "meets_performance_ASR": elapsed <= 5.0
    }, status=200 if confirmed else 409)
