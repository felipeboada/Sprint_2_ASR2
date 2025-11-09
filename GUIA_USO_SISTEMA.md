# 📚 Guía de Uso del Sistema de Logística

## ✅ Problemas Corregidos

### 1. Error al Reabastecer Productos
**Problema anterior**: Faltaba el parámetro `warehouse_name` en la función `restock_atomic()`  
**Solución**: Ahora se obtiene automáticamente el nombre de la bodega desde el formulario

### 2. Error al Crear Pedidos
**Problema anterior**: Faltaban los parámetros `user_lat` y `user_lon`  
**Solución**: Se agregaron campos de ubicación al formulario de pedidos

### 3. Mensajes de Error de Stock
**Solución**: Ahora el sistema muestra mensajes detallados cuando:
- ✅ El pedido se confirma exitosamente (muestra la bodega asignada)
- ❌ No hay suficiente stock disponible
- ❌ Ocurre cualquier error en el proceso

## 🚀 Configuración Inicial

### Paso 1: Crear Datos de Prueba

Ejecuta este comando para crear bodegas, productos e inventario automáticamente:

```bash
python manage.py setup_test_data
```

Esto creará:
- **3 Bodegas**: Norte, Centro, Sur (con ubicaciones reales en Bogotá)
- **8 Productos de Seguridad Industrial (EPP)**: Cascos, Guantes, Gafas, Botas, Chalecos, Mascarillas, Protectores Auditivos, Arneses
- **Inventario Inicial**: 6,780 unidades distribuidas en las bodegas

### Paso 2: Iniciar el Servidor

```bash
python manage.py runserver
```

### Paso 3: Acceder al Sistema

Ve a: http://127.0.0.1:8000/login/

## 👥 Usuarios Disponibles

| Usuario | Contraseña | Rol | Puede hacer |
|---------|-----------|-----|-------------|
| `admin` | `admin123` | Administrador | Todo |
| `operario` | `operario123` | Operario | Gestionar inventario y productos |
| `cliente` | `cliente123` | Cliente | Realizar pedidos |

## 📦 Cómo Reabastecer Productos (Operarios)

1. Inicia sesión como **`operario`**
2. Ve a **"Stock"** en el menú
3. Haz clic en **"Reabastecer"** o ve a: http://127.0.0.1:8000/stockcreate/
4. Completa el formulario:
   - **Producto**: Selecciona el producto
   - **Cantidad**: Unidades a agregar
   - **Unidad**: kg, unidades, etc.
   - **Bodega**: Selecciona la bodega donde agregar stock
5. Envía el formulario

### ✅ Resultado Esperado:
- Mensaje de éxito: "Stock restocked successfully"
- El inventario se actualiza automáticamente

## 🛒 Cómo Crear Pedidos (Clientes)

1. Inicia sesión como **`cliente`**
2. Ve a **"Realizar Pedido"** en el menú o: http://127.0.0.1:8000/ordercreate/
3. Completa el formulario:
   - **Producto**: Selecciona el producto que deseas
   - **Cantidad**: Número de unidades
   - **Latitud**: Tu ubicación (por defecto: centro de Bogotá)
   - **Longitud**: Tu ubicación (por defecto: centro de Bogotá)
4. Haz clic en **"Realizar Pedido"**

### 📍 Ubicaciones de Referencia (Bogotá):
- **Centro**: 4.598889, -74.080833
- **Norte**: 4.710989, -74.072092
- **Sur**: 4.570868, -74.297333

### ✅ Escenarios Posibles:

#### ✅ Pedido Confirmado
Si hay stock suficiente, verás:
```
✓ Pedido #123 confirmado exitosamente.
Producto: Monitor LED 24", Cantidad: 5 unidades.
Bodega asignada: Bodega Norte
```

El sistema automáticamente:
- Busca la bodega más cercana a tu ubicación con stock suficiente
- Asigna la bodega
- Reduce el inventario
- Confirma el pedido

#### ❌ Stock Insuficiente
Si no hay stock, verás:
```
✗ Pedido rechazado: No hay suficiente stock disponible de "Monitor LED 24"".
Solicitaste 500 unidades pero no hay inventario disponible en ninguna bodega.
```

## 📊 Ver Inventario

### Para Operarios y Administradores:
1. Ve a **"Stock"** en el menú
2. Verás una lista completa del inventario con:
   - Producto
   - Bodega
   - Cantidad disponible
   - Última actualización

## 🏢 Gestionar Bodegas (Administradores)

### Opción 1: Django Admin
1. Ve a: http://127.0.0.1:8000/admin/
2. Inicia sesión con `admin` / `admin123`
3. Selecciona **"Warehouses"**
4. Crea, edita o elimina bodegas

### Opción 2: Comando de Management
```bash
# Configurar datos de prueba (incluye bodegas)
python manage.py setup_test_data
```

## 🧪 Casos de Prueba

### Prueba 1: Reabastecimiento Exitoso
1. Inicia sesión como `operario`
2. Ve a "Reabastecer"
3. Selecciona "Casco de Seguridad", 50 unidades, "Bodega Norte"
4. Envía → Deberías ver éxito

### Prueba 2: Pedido con Stock Suficiente
1. Inicia sesión como `cliente`
2. Ve a "Realizar Pedido"
3. Selecciona "Guantes Industriales", 50 unidades
4. Zona de entrega: "Zona Centro"
5. Envía → Pedido confirmado, bodega más cercana asignada

### Prueba 3: Pedido Sin Stock
1. Inicia sesión como `cliente`
2. Intenta pedir 10000 unidades de cualquier producto
3. Envía → Verás mensaje de stock insuficiente

### Prueba 4: Asignación Inteligente de Bodega
1. Crea un pedido de "Mascarilla N95" desde "Zona Norte"
2. El sistema debe asignar "Bodega Norte" (la más cercana con stock)
3. Crea otro pedido desde "Zona Sur"
4. El sistema debe asignar "Bodega Sur" si hay stock disponible

## 🔐 Prueba de Seguridad por Roles

### Prueba 1: Cliente NO puede reabastecer
1. Inicia sesión como `cliente`
2. Intenta acceder a: http://127.0.0.1:8000/stockcreate/
3. Resultado: ❌ "No tienes permisos para acceder a esta página"

### Prueba 2: Operario NO puede gestionar usuarios
1. Inicia sesión como `operario`
2. Intenta acceder a: http://127.0.0.1:8000/admin/
3. Resultado: ❌ Sin acceso (no es staff)

### Prueba 3: Admin tiene acceso completo
1. Inicia sesión como `admin`
2. Puedes acceder a todas las secciones ✅

## 📈 Inventario de Prueba Disponible (EPP - Equipos de Protección Personal)

| Producto | Bodega Norte | Bodega Centro | Bodega Sur | Total |
|----------|--------------|---------------|------------|-------|
| Casco de Seguridad | 150 | 200 | 100 | 450 |
| Guantes Industriales | 500 | 400 | 300 | 1,200 |
| Gafas de Protección | 250 | 300 | 0 | 550 |
| Botas de Seguridad | 120 | 0 | 80 | 200 |
| Chaleco Reflectivo | 0 | 350 | 200 | 550 |
| Mascarilla N95 | 1,000 | 1,500 | 800 | 3,300 |
| Protector Auditivo | 180 | 220 | 0 | 400 |
| Arnés de Seguridad | 60 | 40 | 30 | 130 |

**Total General**: 6,780 unidades

## 🔄 Reiniciar Datos de Prueba

Si quieres reiniciar todo el inventario:

```bash
# Eliminar la base de datos
rm db.sqlite3

# Recrear con migraciones
python manage.py migrate

# Crear usuarios
python manage.py create_test_users

# Crear datos de prueba
python manage.py setup_test_data
```

## 🛠️ Comandos Útiles

```bash
# Ver todos los usuarios
python manage.py shell
>>> from authentication.models import User
>>> User.objects.all()

# Ver inventario
>>> from orders.models import Inventory
>>> for inv in Inventory.objects.all():
...     print(f"{inv.product.name} @ {inv.warehouse.name}: {inv.quantity}")

# Ver pedidos
>>> from orders.models import Order
>>> Order.objects.all()

# Ver pedidos confirmados
>>> Order.objects.filter(status='CONFIRMED')

# Ver pedidos rechazados
>>> Order.objects.filter(status='REJECTED')
```

## 📝 Estructura de la Base de Datos

### Modelos Principales:

1. **User** (authentication)
   - username, email, password (hash)
   - role: ADMIN, OPERARIO, CLIENTE

2. **Warehouse** (orders)
   - name, latitude, longitude

3. **Product** (orders)
   - name

4. **Variable** (products)
   - name, product (ForeignKey)

5. **Inventory** (orders)
   - product, warehouse, quantity

6. **Order** (orders)
   - product, units, status, assigned_warehouse

## 🎯 Características del Sistema

### ✅ Autenticación y Autorización
- Login seguro con contraseñas hasheadas
- 3 roles con permisos diferenciados
- Menú dinámico según rol
- Protección de vistas por decoradores

### ✅ Gestión de Inventario
- Reabastecimiento por bodega
- Vista en tiempo real del stock
- Actualización automática al confirmar pedidos

### ✅ Sistema de Pedidos Inteligente
- Asignación automática de bodega más cercana
- Verificación de stock en múltiples bodegas
- Mensajes detallados de confirmación/rechazo
- Cálculo de distancia con fórmula Haversine

### ✅ Transacciones Atómicas
- Operaciones de inventario son atómicas
- No se pierde consistencia de datos
- Reintentos automáticos en caso de conflicto

## 🐛 Solución de Problemas

### "No hay productos en el formulario"
**Solución**: Ejecuta `python manage.py setup_test_data`

### "No hay bodegas disponibles"
**Solución**: Ejecuta `python manage.py setup_test_data` o crea bodegas manualmente en el admin

### "place_order_atomic() missing arguments"
**Solución**: Ya corregido, actualiza el código

### "restock_atomic() missing warehouse_name"
**Solución**: Ya corregido, actualiza el código

---

**Última actualización**: Noviembre 2025  
**Versión**: 2.0  
**Estado**: ✅ Completamente funcional

