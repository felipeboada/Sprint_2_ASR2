from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(*roles):
    """
    Decorador para verificar que el usuario tenga uno de los roles especificados.
    
    Uso:
        @role_required('ADMIN', 'OPERARIO')
        def mi_vista(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.has_role(*roles):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request, 
                    f'No tienes permisos para acceder a esta página. '
                    f'Se requiere el rol: {", ".join(roles)}'
                )
                return redirect('/')
        return wrapper
    return decorator

def admin_required(view_func):
    """
    Decorador para vistas que solo pueden acceder administradores.
    
    Uso:
        @admin_required
        def mi_vista_admin(request):
            ...
    """
    return role_required('ADMIN')(view_func)

def operario_required(view_func):
    """
    Decorador para vistas que pueden acceder operarios y administradores.
    
    Uso:
        @operario_required
        def mi_vista_operario(request):
            ...
    """
    return role_required('ADMIN', 'OPERARIO')(view_func)

def cliente_required(view_func):
    """
    Decorador para vistas que pueden acceder clientes.
    
    Uso:
        @cliente_required
        def mi_vista_cliente(request):
            ...
    """
    return role_required('ADMIN', 'CLIENTE')(view_func)

