from typing import Optional, Tuple
from math import radians, cos, sin, asin, sqrt
from django.db import transaction, DatabaseError
from django.db.models import F
from .models import Inventory, Order, Product, Warehouse


def create_or_get_product(name: str) -> Product:

    product, _ = Product.objects.get_or_create(name=name) #obtiene o crea un producto por nombre
    
    return product

def haversine_km(lon1, lat1, lon2, lat2) -> float: #retorna la distancia en km entre dos puntos geograficos

    R= 6371.0 #radio de la tierra en km
    dlon = radians(lon2 - lon1)
    dlat = radians(lat2 - lat1)
    a=sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 2*R*asin(sqrt(a)) #retorna la distancia en km

def find_nearest_with_stock(product: Product, units: int, user_lat: float, user_lon: float) -> Optional[Inventory]: #encuentra la bodega mas cercana con stock suficiente para un producto y unidades dadas

    qs = (Inventory.objects.select_related('warehouse').filter(product=product, quantity__gte=units)) #filtra inventarios con stock suficiente segun el producto y unidades
    
    if not qs.exists(): return None
    
    return min(qs, key=lambda inv: haversine_km(user_lat, user_lon, inv.warehouse.latitude, inv.warehouse.longitude)) #retorna el inventario con la bodega mas cercana



def place_order_atomic(product_name: str, units: int, user_lat: float, user_lon: float, main_warehouse_name: Optional[str]=None, max_retries:int=3) -> Tuple[Order, bool]:
    #funcion para realizar un pedido de manera atomica, retorna la orden y un booleano que indica si fue confirmada o rechazada
    
    if units<=0: raise ValueError("units must be > 0")
    product = create_or_get_product(product_name)

    for attempt in range(1, max_retries+1):

        try:

            with transaction.atomic():

                order = Order.objects.create(product=product, units=units)


                # 1) si se especifica bodega principal, intenta ahí

                if main_warehouse_name:
                    try:
                        mw = Warehouse.objects.get(name=main_warehouse_name)

                        inv = (Inventory.objects.select_for_update().get(product=product, warehouse=mw))

                        if inv.quantity >= units:

                            Inventory.objects.filter(pk=inv.pk, quantity__gte=units)\
                                .update(quantity=F('quantity')-units)
                            
                            order.status = Order.CONFIRMED
                            order.assigned_warehouse = mw
                            order.save(update_fields=['status','assigned_warehouse'])
                            
                            return order, True
                    except (Warehouse.DoesNotExist, Inventory.DoesNotExist):
                        pass

                # 2) alternativa: bodega más cercana con stock
                
                alt = find_nearest_with_stock(product, units, user_lat, user_lon)

                if alt:

                    alt = Inventory.objects.select_for_update().get(pk=alt.pk)
                    
                    if alt.quantity >= units:

                        Inventory.objects.filter(pk=alt.pk, quantity__gte=units)\
                            .update(quantity=F('quantity')-units)
                        
                        order.status = Order.CONFIRMED
                        order.assigned_warehouse = alt.warehouse
                        order.save(update_fields=['status','assigned_warehouse'])
                        
                        return order, True
                        

                # 3) sin stock
                
                order.status = Order.REJECTED
                order.save(update_fields=['status'])
                return order, False
            

        except DatabaseError:
            if attempt >= max_retries: raise
            continue



    """
ASR: Verificar disponibilidad en múltiples bodegas y asignar automáticamente la más cercana con stock.

Comportamiento:
- Verifica si hay stock en la bodega principal (si se indica).
- Si no hay, busca automáticamente la bodega más cercana al usuario con unidades suficientes.
- Si ninguna tiene stock, la orden queda REJECTED.
- Todo se ejecuta de forma atómica y en menos de 5 segundos.
"""


def restock_atomic(product_name: str, units: int, warehouse_name:str) -> Inventory: #añade stock a una bodega específica
    if units<=0: raise ValueError("units must be > 0")
    product = create_or_get_product(product_name)
    wh,_ = Warehouse.objects.get_or_create(name=warehouse_name, defaults={"latitude":0.0,"longitude":0.0})
    with transaction.atomic():
        inv,_ = Inventory.objects.select_for_update().get_or_create(product=product, warehouse=wh)
        Inventory.objects.filter(pk=inv.pk).update(quantity=F('quantity')+units)
        inv.refresh_from_db()
        return inv

def get_inventory(product_name: str): #obtiene el inventario de un producto específico
    product = create_or_get_product(product_name)
    return Inventory.objects.select_related('product','warehouse').filter(product=product)


