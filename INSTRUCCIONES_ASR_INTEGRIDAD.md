# 🚀 Instrucciones de Uso - ASR de Integridad de Datos

## ✅ Sistema Implementado

El ASR de Integridad de Datos está completamente implementado y las migraciones se han aplicado exitosamente.

---

## 📦 ¿Qué se ha implementado?

### 1. Módulo de Validadores (`orders/validators.py`)
- ✅ Validadores de formato (teléfono, NIT, coordenadas, direcciones, nombres)
- ✅ Validadores numéricos (cantidades positivas, no negativas)
- ✅ Validadores de reglas de negocio (stock, capacidad de bodega)

### 2. Modelos con Validaciones Completas

#### ✅ Proveedor (Supplier)
- Nuevo modelo con 13 campos validados
- NIT con formato colombiano
- Email y teléfono únicos
- Calificación de 0 a 5
- Días de crédito máximo 365

#### ✅ Producto (Product) - Mejorado
- 15 campos (8 nuevos)
- Validación de precios (venta >= costo)
- Validación de stock (mínimo <= máximo)
- SKU único en mayúsculas
- Relación con proveedor activo

#### ✅ Bodega (Warehouse) - Mejorado
- 10 campos (6 nuevos)
- Coordenadas validadas para Colombia
- Capacidad por defecto 50,000 unidades
- Métodos de capacidad disponible

#### ✅ Inventario (Inventory) - Mejorado
- 7 campos (2 nuevos)
- Cantidad reservada controlada
- Validación de capacidad de bodega
- Métodos de reserva y liberación

#### ✅ Pedido (Order) - Mejorado
- 14 campos (9 nuevos)
- 6 estados con transiciones controladas
- Validación de stock al confirmar
- Precio total automático
- Control de fechas

#### ✅ Cliente (User) - Mejorado
- 8 campos adicionales
- Documento único
- Clientes requieren email y teléfono
- Validación de roles

### 3. Serializadores API con Validaciones
- ✅ SupplierSerializer
- ✅ ProductSerializer con margen de ganancia
- ✅ WarehouseSerializer con capacidad
- ✅ InventorySerializer con disponibilidad
- ✅ OrderSerializer con estados

### 4. Administración Django
- ✅ Admin de Proveedores registrado
- ✅ Admins actualizados con nuevos campos

### 5. Documentación
- ✅ ASR_INTEGRIDAD_DATOS.md completo
- ✅ Este documento de instrucciones

---

## 🎯 Cómo Usar el Sistema

### 1. Verificar que el servidor esté corriendo

```bash
cd "C:\Users\USER\Documents\TODO\universidad\6to semestre\Arquisoft\Sprint_2_ASR2"
venv\Scripts\python.exe manage.py runserver
```

### 2. Acceder al Panel de Administración

1. Ir a: http://127.0.0.1:8000/admin/
2. Iniciar sesión con usuario administrador
3. Verás las siguientes secciones:
   - **ORDERS**: Proveedores, Productos, Bodegas, Inventarios, Pedidos
   - **AUTHENTICATION**: Usuarios

### 3. Crear un Proveedor

```python
# Desde el admin de Django o usando Python shell:
from orders.models import Supplier

supplier = Supplier.objects.create(
    name="Distribuidora ABC S.A.S.",
    nit="900123456-7",
    email="contacto@abc.com",
    phone="3001234567",
    address="Calle 123 #45-67",
    city="Bogotá",
    contact_person="Juan Pérez",
    credit_days=30,
    rating=4.5,
    is_active=True
)
```

### 4. Crear un Producto con Proveedor

```python
from orders.models import Product, Supplier

supplier = Supplier.objects.get(nit="900123456-7")

product = Product.objects.create(
    name="Casco de Seguridad Industrial",
    sku="CSI-001",
    description="Casco de seguridad clase A",
    supplier=supplier,
    unit_price=45000,
    cost_price=30000,
    category="EPP",
    min_stock=50,
    max_stock=500,
    is_active=True
)
```

### 5. Agregar Inventario

```python
from orders.models import Inventory, Product, Warehouse

product = Product.objects.get(sku="CSI-001")
warehouse = Warehouse.objects.first()

inventory = Inventory.objects.create(
    product=product,
    warehouse=warehouse,
    quantity=200,
    reserved_quantity=0
)
```

### 6. Crear un Pedido

```python
from orders.models import Order, Product, Warehouse
from authentication.models import User

product = Product.objects.get(sku="CSI-001")
warehouse = Warehouse.objects.first()
customer = User.objects.filter(role='CLIENTE').first()

order = Order.objects.create(
    product=product,
    units=10,
    assigned_warehouse=warehouse,
    customer=customer,
    delivery_address="Calle 45 #12-34, Bogotá",
    delivery_zone="centro",
    status=Order.PENDING
)

# El precio total se calcula automáticamente
print(f"Total: ${order.total_price}")
```

---

## ⚠️ Validaciones Automáticas

### Ejemplos de Validaciones que se Ejecutan:

#### 1. Precio de Venta < Precio de Costo
```python
product = Product(
    name="Producto Test",
    unit_price=30000,  # ❌ Menor que costo
    cost_price=35000
)
product.save()  
# ValidationError: 'El precio de venta no puede ser menor al precio de costo'
```

#### 2. NIT Inválido
```python
supplier = Supplier(
    name="Test",
    nit="12345",  # ❌ Formato inválido
    email="test@test.com",
    phone="3001234567",
    address="Calle 1",
    city="Bogotá",
    contact_person="Juan"
)
supplier.save()
# ValidationError: 'NIT inválido. Formato correcto: 123456789-0'
```

#### 3. Stock Insuficiente en Pedido
```python
order = Order(
    product=product,
    units=1000,  # ❌ Más de lo disponible
    status=Order.CONFIRMED,
    assigned_warehouse=warehouse
)
order.save()
# ValidationError: 'Stock insuficiente. Disponible: 200, Solicitado: 1000'
```

#### 4. Coordenadas Fuera de Rango
```python
warehouse = Warehouse(
    name="Bodega Test",
    latitude=50.0,  # ❌ Fuera de Colombia
    longitude=-80.0
)
warehouse.save()
# ValidationError: 'Latitud fuera del rango válido para Colombia (-4.5 a 13.5)'
```

---

## 🔄 API REST con Validaciones

### Endpoints Disponibles

```bash
# Proveedores
GET    /api/suppliers/          # Listar proveedores
POST   /api/suppliers/          # Crear proveedor
GET    /api/suppliers/{id}/     # Ver proveedor
PUT    /api/suppliers/{id}/     # Actualizar proveedor
DELETE /api/suppliers/{id}/     # Eliminar proveedor

# Productos
GET    /api/products/           # Listar productos
POST   /api/products/           # Crear producto
GET    /api/products/{id}/      # Ver producto
PUT    /api/products/{id}/      # Actualizar producto
DELETE /api/products/{id}/      # Eliminar producto

# Similar para: warehouses, inventory, orders
```

### Ejemplo de Request con Validación

```bash
# POST /api/products/
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Casco",
    "sku": "CSC-001",
    "unit_price": 45000,
    "cost_price": 30000,
    "min_stock": 50,
    "max_stock": 500
  }'

# Respuesta exitosa:
{
  "id": 1,
  "name": "Casco",
  "sku": "CSC-001",
  "unit_price": "45000.00",
  "cost_price": "30000.00",
  "profit_margin": 50.0,
  "created_at": "2025-11-13T01:30:00Z"
}
```

---

## 🧪 Testing de Validaciones

### Probar desde Django Shell

```bash
venv\Scripts\python.exe manage.py shell
```

```python
# Test 1: Validación de NIT
from orders.models import Supplier
from django.core.exceptions import ValidationError

try:
    s = Supplier(name="Test", nit="invalid", email="t@t.com", 
                 phone="3001234567", address="Calle 1", 
                 city="Bogotá", contact_person="Juan")
    s.save()
except ValidationError as e:
    print("✅ Validación funcionó:", e.message_dict)

# Test 2: Validación de precios
from orders.models import Product

try:
    p = Product(name="Test", unit_price=100, cost_price=200)
    p.save()
except ValidationError as e:
    print("✅ Validación funcionó:", e.message_dict)

# Test 3: Ver métodos de negocio
product = Product.objects.first()
print(f"Stock total: {product.get_total_stock()}")
print(f"Margen: {product.get_profit_margin()}%")

warehouse = Warehouse.objects.first()
print(f"Capacidad disponible: {warehouse.get_available_capacity()}")
```

---

## 📊 Verificar Datos del Sistema

### Ver Proveedores
```python
from orders.models import Supplier

for s in Supplier.objects.all():
    print(f"{s.name} - {s.nit} - Rating: {s.rating}")
```

### Ver Productos con Stock
```python
from orders.models import Product

for p in Product.objects.filter(is_active=True):
    stock = p.get_total_stock()
    margin = p.get_profit_margin()
    print(f"{p.name}: Stock={stock}, Margen={margin:.2f}%")
    if p.is_below_min_stock():
        print(f"  ⚠️ ALERTA: Stock bajo mínimo!")
```

### Ver Pedidos por Estado
```python
from orders.models import Order

pending = Order.objects.filter(status=Order.PENDING).count()
confirmed = Order.objects.filter(status=Order.CONFIRMED).count()
delivered = Order.objects.filter(status=Order.DELIVERED).count()

print(f"Pendientes: {pending}")
print(f"Confirmados: {confirmed}")
print(f"Entregados: {delivered}")
```

---

## 🔧 Resolución de Problemas

### Problema: Validación demasiado estricta

Si necesitas crear datos sin validación (por ejemplo, para migraciones o testing):

```python
# Usar skip_validation=True
warehouse.save(skip_validation=True)
```

### Problema: Datos existentes no válidos

Para encontrar y corregir datos existentes:

```python
from orders.models import Product
from django.core.exceptions import ValidationError

for p in Product.objects.all():
    try:
        p.full_clean()
    except ValidationError as e:
        print(f"Producto {p.id}: {e.message_dict}")
```

---

## 📚 Documentación Completa

Para más detalles, consulta:
- **ASR_INTEGRIDAD_DATOS.md**: Especificación completa del ASR
- **orders/validators.py**: Código de validadores
- **orders/models.py**: Modelos con validaciones
- **orders/serializers.py**: Serializadores de API

---

## ✨ Resumen de Beneficios

1. ✅ **Datos Completos**: Todos los campos obligatorios validados
2. ✅ **Datos Válidos**: Formatos correctos (NIT, teléfono, email, coordenadas)
3. ✅ **Datos Consistentes**: Relaciones válidas entre entidades
4. ✅ **Reglas de Negocio**: Automáticamente aplicadas
5. ✅ **Prevención de Errores**: Validación en múltiples capas
6. ✅ **Mensajes Claros**: Errores descriptivos en español
7. ✅ **API Segura**: Validación automática en endpoints REST
8. ✅ **Auditoría**: Timestamps automáticos en todos los modelos

---

**¡El sistema PROVESI S.A.S. ahora cuenta con un robusto sistema de validación de integridad de datos!** 🎉

