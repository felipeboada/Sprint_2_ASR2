# orders/views.py
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from .logic import get_inventory, restock_atomic, place_order_atomic
from .serializers import InventorySerializer, OrderSerializer
from django.http import JsonResponse
from .logic import place_order_atomic
from django.views.decorators.csrf import csrf_exempt

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
@require_http_methods(["GET", "POST"])
def create_order_view(request):
    """
    Vista para crear una orden automática que verifica disponibilidad
    y asigna la bodega más cercana con stock.
    Permite GET (pruebas rápidas por URL) y POST (con JSON desde Postman).
    """

    try:
        if request.method == "POST":
            payload = json.loads(request.body.decode("utf-8")) if request.body else {}
            product_name = payload.get("product", "Mouse inalámbrico")
            units = int(payload.get("units", 3))
            user_lat = float(payload.get("lat", 4.6097))
            user_lon = float(payload.get("lon", -74.0817))
            main_warehouse = payload.get("main", None)
        else:
            # Permite probar desde el navegador con parámetros GET
            product_name = request.GET.get("product", "Mouse inalámbrico")
            units = int(request.GET.get("units", 3))
            user_lat = float(request.GET.get("lat", 4.6097))
            user_lon = float(request.GET.get("lon", -74.0817))
            main_warehouse = request.GET.get("main", None)

        order, confirmed = place_order_atomic(
            product_name, units, user_lat, user_lon, main_warehouse
        )

        data = {
            "order_id": order.id,
            "product": order.product.name,
            "units": order.units,
            "status": order.status,
            "assigned_warehouse": order.assigned_warehouse.name if order.assigned_warehouse else None,
            "confirmed": confirmed,
        }

        return JsonResponse(data, status=200)

    except Exception as e:
        return HttpResponseBadRequest(str(e))