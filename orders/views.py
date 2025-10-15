import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from .logic import get_inventory, restock_atomic, place_order_atomic
from .serializers import InventorySerializer, OrderSerializer


@require_http_methods(["GET"])
def inventory_detail(request, product_name: str):
    inventory = get_inventory(product_name)
    data = InventorySerializer(inventory).data
    return JsonResponse(data, status=200)


@require_http_methods(["POST"])
def inventory_restock(request, product_name: str):
    try:
        payload = json.loads(request.body.decode("utf-8")) if request.body else {}
        units = int(payload.get("units", 0))
    except (ValueError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid payload")

    inventory = restock_atomic(product_name, units)
    data = InventorySerializer(inventory).data
    return JsonResponse(data, status=200)


@require_http_methods(["POST"])
def place_order(request, product_name: str):
    try:
        payload = json.loads(request.body.decode("utf-8")) if request.body else {}
        units = int(payload.get("units", 0))
    except (ValueError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid payload")

    order, confirmed = place_order_atomic(product_name, units)
    data = OrderSerializer(order).data
    return JsonResponse({"order": data, "confirmed": confirmed}, status=200 if confirmed else 409)
