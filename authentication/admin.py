from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuración del panel de administración para el modelo User"""
    
    list_display = ('username_display', 'full_name', 'email', 'role_badge', 'contact_info', 'status_badge', 'staff_badge')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'city')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'document_number')
    ordering = ('username',)
    list_per_page = 25
    
    fieldsets = (
        ('Autenticación', {
            'fields': ('username', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Rol y Permisos', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Contacto', {
            'fields': ('phone', 'address', 'city')
        }),
        ('Documentación', {
            'fields': ('document_type', 'document_number'),
            'classes': ('collapse',)
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Información de Cuenta', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
        ('Rol', {
            'fields': ('role', 'is_staff', 'is_superuser')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'phone', 'address', 'city')
        }),
    )
    
    @admin.display(description='Usuario', ordering='username')
    def username_display(self, obj):
        icon = '👑' if obj.is_superuser else '🔧' if obj.is_staff else '👤'
        return format_html(f'{icon} <b>{obj.username}</b>')
    
    @admin.display(description='Nombre Completo')
    def full_name(self, obj):
        name = obj.get_full_name()
        if name:
            return format_html(f'{name}')
        return format_html('<span style="color: #6c757d;">-</span>')
    
    @admin.display(description='Rol', ordering='role')
    def role_badge(self, obj):
        colors = {
            'ADMIN': '#dc3545',
            'OPERARIO': '#17a2b8',
            'CLIENTE': '#28a745',
        }
        icons = {
            'ADMIN': '⚙️',
            'OPERARIO': '🔧',
            'CLIENTE': '🛒',
        }
        color = colors.get(obj.role, '#6c757d')
        icon = icons.get(obj.role, '•')
        return format_html(
            f'<span style="color: white; background-color: {color}; padding: 3px 10px; border-radius: 3px;">'
            f'{icon} {obj.get_role_display()}</span>'
        )
    
    @admin.display(description='Contacto')
    def contact_info(self, obj):
        if obj.phone:
            return format_html(f'📞 {obj.phone}')
        return format_html('<span style="color: #6c757d;">Sin teléfono</span>')
    
    @admin.display(description='Estado', ordering='is_active')
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: white; background-color: #28a745; padding: 3px 10px; border-radius: 3px;">✓ Activo</span>')
        return format_html('<span style="color: white; background-color: #dc3545; padding: 3px 10px; border-radius: 3px;">✗ Inactivo</span>')
    
    @admin.display(description='Staff', ordering='is_staff')
    def staff_badge(self, obj):
        if obj.is_superuser:
            return format_html('<span style="color: white; background-color: #6f42c1; padding: 3px 10px; border-radius: 3px;">👑 Superusuario</span>')
        elif obj.is_staff:
            return format_html('<span style="color: white; background-color: #fd7e14; padding: 3px 10px; border-radius: 3px;">🔧 Staff</span>')
        return format_html('<span style="color: #6c757d;">-</span>')
