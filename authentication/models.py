from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Modelo de Usuario extendido con roles para control de acceso.
    Roles disponibles: ADMIN, OPERARIO, CLIENTE
    """
    
    ADMIN = 'ADMIN'
    OPERARIO = 'OPERARIO'
    CLIENTE = 'CLIENTE'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (OPERARIO, 'Operario'),
        (CLIENTE, 'Cliente'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=CLIENTE,
        verbose_name='Rol'
    )
    
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    address = models.TextField(blank=True, null=True, verbose_name='Dirección')
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        return self.role == self.ADMIN
    
    def is_operario(self):
        """Verifica si el usuario es operario"""
        return self.role == self.OPERARIO
    
    def is_cliente(self):
        """Verifica si el usuario es cliente"""
        return self.role == self.CLIENTE
    
    def has_role(self, *roles):
        """Verifica si el usuario tiene alguno de los roles especificados"""
        return self.role in roles
