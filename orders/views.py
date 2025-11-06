# orders/views.py
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
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
