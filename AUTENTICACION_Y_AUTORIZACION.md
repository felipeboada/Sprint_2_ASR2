# Sistema de Autenticación y Autorización por Roles

## 📋 Descripción del ASR Implementado

Este sistema cumple con el siguiente Atributo de Calidad de Software (ASR):

> "Como administrador del sistema, quiero que todos los usuarios (operarios, clientes y administradores) accedan mediante autenticación segura y con permisos diferenciados según su rol, para proteger la información de pedidos, inventario y pagos, y prevenir accesos no autorizados. Los controles de acceso deben impedir que un usuario ejecute funciones fuera de su rol definido. Además, los usuarios y las contraseñas deben ser almacenados en la base de datos para tener acceso en cualquier momento a las credenciales."

## 🔐 Componentes Implementados

### 1. Modelo de Usuario Extendido

Se creó un modelo personalizado de usuario que extiende `AbstractUser` de Django con los siguientes roles:

- **ADMIN (Administrador)**: Acceso completo al sistema
- **OPERARIO**: Gestión de inventario y productos
- **CLIENTE**: Realización de pedidos y consulta de productos

**Archivo**: `authentication/models.py`

### 2. Sistema de Autenticación

- **Login seguro**: Formulario de autenticación con validación
- **Logout**: Cierre de sesión seguro
- **Perfil de usuario**: Vista de información del usuario y sus permisos

**Archivos**:
- `authentication/views.py`
- `authentication/templates/authentication/login.html`
- `authentication/templates/authentication/profile.html`

### 3. Control de Acceso por Roles

Se implementaron decoradores para proteger las vistas según el rol:

- `@admin_required`: Solo administradores
- `@operario_required`: Operarios y administradores
- `@cliente_required`: Clientes y administradores
- `@role_required('ROL1', 'ROL2', ...)`: Múltiples roles personalizados

**Archivo**: `authentication/decorators.py`

### 4. Protección de Vistas

Todas las vistas del sistema están protegidas según el rol:

#### Inventory (Stock)
- `measurement_list` - Ver stock: **@operario_required**
- `measurement_create` - Crear/Reabastecer stock: **@operario_required**
- `measurement_order_create` - Crear pedidos: **@cliente_required**

#### Products
- `variable_list` - Ver productos: **@login_required** (todos los roles autenticados)
- `variable_create` - Crear productos: **@operario_required**

#### Orders (API REST)
- Las vistas de API pueden ser accedidas por usuarios autenticados

### 5. Interfaz de Usuario Diferenciada

El menú de navegación se adapta según el rol del usuario:

**Administradores**:
- Productos
- Stock
- Crear Pedido
- Administración (Django Admin)

**Operarios**:
- Productos
- Stock
- Reabastecer

**Clientes**:
- Catálogo
- Realizar Pedido

## 👥 Usuarios de Prueba

El sistema incluye usuarios de prueba precreados:

| Usuario | Contraseña | Rol | Descripción |
|---------|-----------|-----|-------------|
| `admin` | `admin123` | Administrador | Acceso completo al sistema |
| `operario` | `operario123` | Operario | Gestión de inventario y productos |
| `cliente` | `cliente123` | Cliente | Realización de pedidos |

## 🚀 Cómo Usar el Sistema

### Iniciar Sesión

1. Accede a: http://127.0.0.1:8000/login/
2. Ingresa uno de los usuarios de prueba
3. Serás redirigido al dashboard según tu rol

### Crear Nuevos Usuarios

#### Opción 1: Django Admin (Solo Administradores)
1. Accede a: http://127.0.0.1:8000/admin/
2. Inicia sesión con el usuario `admin`
3. Ve a "Usuarios" y crea un nuevo usuario
4. Asigna el rol correspondiente

#### Opción 2: Comando de Management
```bash
python manage.py create_test_users
```

## 🔒 Características de Seguridad

### 1. Almacenamiento Seguro de Contraseñas
- Las contraseñas se almacenan usando **hash bcrypt** de Django
- Nunca se almacenan contraseñas en texto plano
- El sistema usa `PBKDF2` con SHA256 por defecto

### 2. Protección CSRF
- Todas las formas incluyen tokens CSRF
- Prevención de ataques de falsificación de peticiones entre sitios

### 3. Control de Acceso
- Verificación de permisos a nivel de vista
- Mensajes de error informativos cuando no se tienen permisos
- Redirección automática al login para usuarios no autenticados

### 4. Sesiones Seguras
- Gestión de sesiones de Django
- Timeout automático configurable
- Logout seguro que invalida la sesión

## 📁 Estructura de Archivos

```
authentication/
├── __init__.py
├── models.py                    # Modelo User con roles
├── admin.py                     # Configuración admin
├── views.py                     # Vistas de login/logout/profile
├── urls.py                      # URLs de autenticación
├── decorators.py                # Decoradores de control de acceso
├── apps.py
├── templates/
│   └── authentication/
│       ├── login.html          # Página de login
│       └── profile.html        # Página de perfil
└── management/
    └── commands/
        └── create_test_users.py # Comando para crear usuarios

logistics/
├── settings.py                  # Configuración AUTH_USER_MODEL
├── urls.py                      # URLs principales
└── templates/
    └── base.html               # Template base con menú dinámico

inventory/views.py              # Vistas protegidas con decoradores
products/views.py               # Vistas protegidas con decoradores
orders/views.py                 # Vistas de API protegidas
```

## 🧪 Pruebas del Sistema

### Prueba 1: Autenticación
1. Accede a cualquier página protegida sin estar logueado
2. Deberías ser redirigido al login
3. Inicia sesión con credenciales válidas
4. Deberías acceder a la página solicitada

### Prueba 2: Autorización por Roles - Cliente
1. Inicia sesión como `cliente`
2. Intenta acceder a `/stock/`
3. Deberías ver un mensaje de "No tienes permisos"
4. Accede a `/ordercreate/` - Deberías tener acceso

### Prueba 3: Autorización por Roles - Operario
1. Inicia sesión como `operario`
2. Accede a `/stock/` - Deberías tener acceso
3. Accede a `/productos/` - Deberías tener acceso
4. Intenta acceder a `/admin/` - Sin acceso (no es staff)

### Prueba 4: Autorización por Roles - Admin
1. Inicia sesión como `admin`
2. Deberías tener acceso a todas las secciones
3. Incluyendo `/admin/` (Django Admin)

### Prueba 5: Menú Dinámico
1. Inicia sesión con cada uno de los roles
2. Verifica que el menú de navegación muestre solo las opciones permitidas
3. El badge del usuario debe mostrar el rol correcto

## 📊 Cumplimiento del ASR

### ✅ Requisitos Cumplidos

| Requisito | Implementación | Estado |
|-----------|----------------|--------|
| Autenticación segura | Sistema de login con Django Auth | ✅ |
| 3 roles diferenciados | Admin, Operario, Cliente | ✅ |
| Permisos por rol | Decoradores personalizados | ✅ |
| Protección de información | Vistas protegidas con decoradores | ✅ |
| Prevención de accesos no autorizados | Login requerido + verificación de roles | ✅ |
| Controles de acceso | Usuario no puede ejecutar funciones fuera de su rol | ✅ |
| Almacenamiento en BD | Modelo User en base de datos | ✅ |
| Contraseñas seguras | Hash con algoritmo PBKDF2-SHA256 | ✅ |
| Acceso a credenciales | Panel de admin para gestión de usuarios | ✅ |

## 🔄 Flujo de Autenticación y Autorización

```
┌──────────────┐
│   Usuario    │
└──────┬───────┘
       │
       ├──> GET /productos/
       │
┌──────▼────────────────────────────┐
│  1. Verificación de autenticación │
│     (@login_required)              │
└──────┬────────────────────────────┘
       │
       ├─ No autenticado ──> Redirect a /login/
       │
       ├─ Autenticado ──> Continuar
       │
┌──────▼────────────────────────────┐
│  2. Verificación de autorización  │
│     (@operario_required)           │
└──────┬────────────────────────────┘
       │
       ├─ Sin permisos ──> Mensaje de error + Redirect a /
       │
       ├─ Con permisos ──> Ejecutar vista
       │
┌──────▼────────────────────────────┐
│  3. Renderizar respuesta           │
└────────────────────────────────────┘
```

## 🛠️ Comandos Útiles

```bash
# Crear usuarios de prueba
python manage.py create_test_users

# Crear un superusuario manualmente
python manage.py createsuperuser

# Ver usuarios en la base de datos
python manage.py shell
>>> from authentication.models import User
>>> User.objects.all()

# Cambiar rol de un usuario
>>> user = User.objects.get(username='nombre_usuario')
>>> user.role = User.ADMIN
>>> user.save()

# Cambiar contraseña de un usuario
>>> user = User.objects.get(username='nombre_usuario')
>>> user.set_password('nueva_contraseña')
>>> user.save()
```

## 📝 Notas Adicionales

1. **Sesiones**: Las sesiones expiran automáticamente según la configuración de Django
2. **Escalabilidad**: El sistema puede extenderse con más roles fácilmente
3. **API REST**: Las vistas de API también están protegidas con autenticación
4. **Personalización**: Los decoradores permiten combinaciones flexibles de roles

## 🎯 Próximas Mejoras

- [ ] Implementar recuperación de contraseña
- [ ] Agregar autenticación de dos factores (2FA)
- [ ] Registro de auditoría de accesos
- [ ] Límite de intentos de login
- [ ] Expiración de contraseñas periódica
- [ ] Permisos granulares a nivel de objeto

---

**Fecha de implementación**: Noviembre 2025  
**Versión**: 1.0  
**Estado**: ✅ Completado y funcional

