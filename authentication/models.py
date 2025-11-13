from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from orders.validators import validate_phone_number, validate_address_format, validate_name_format


class User(AbstractUser):
    ADMIN = 'ADMIN'
    OPERARIO = 'OPERARIO'
    CLIENTE = 'CLIENTE'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (OPERARIO, 'Operario'),
        (CLIENTE, 'Cliente'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CLIENTE)
    phone = models.CharField(max_length=20, blank=True, null=True, validators=[validate_phone_number])
    address = models.TextField(blank=True, null=True, validators=[validate_address_format])
    document_type = models.CharField(
        max_length=10,
        choices=[('CC', 'Cédula'), ('CE', 'Extranjería'), ('NIT', 'NIT'), ('PASSPORT', 'Pasaporte')],
        blank=True, null=True
    )
    document_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']
        indexes = [
            models.Index(fields=['username']), models.Index(fields=['email']),
            models.Index(fields=['role']), models.Index(fields=['document_number'])
        ]
    
    def clean(self):
        errors = {}
        if self.username:
            self.username = self.username.strip().lower()
            if len(self.username) < 4:
                errors['username'] = 'El nombre de usuario debe tener al menos 4 caracteres'
            if User.objects.filter(username=self.username).exclude(pk=self.pk).exists():
                errors['username'] = 'Ya existe un usuario con este nombre'
        
        if self.email:
            self.email = self.email.strip().lower()
            if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
                errors['email'] = 'Ya existe un usuario con este email'
        
        if self.first_name:
            self.first_name = self.first_name.strip()
            try:
                validate_name_format(self.first_name)
            except ValidationError as e:
                errors['first_name'] = e.message
        
        if self.last_name:
            self.last_name = self.last_name.strip()
            try:
                validate_name_format(self.last_name)
            except ValidationError as e:
                errors['last_name'] = e.message
        
        if self.document_number:
            self.document_number = self.document_number.strip()
            if not self.document_type:
                errors['document_type'] = 'Debe especificar el tipo de documento'
            if User.objects.filter(document_number=self.document_number).exclude(pk=self.pk).exists():
                errors['document_number'] = 'Ya existe un usuario con este documento'
        
        if self.role == self.CLIENTE:
            if not self.email:
                errors['email'] = 'Los clientes deben tener un email'
            if not self.phone:
                errors['phone'] = 'Los clientes deben tener un teléfono'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        if kwargs.pop('skip_validation', False):
            super().save(*args, **kwargs)
            return
        
        if not self.pk or (self.password and self.password.startswith('pbkdf2_')):
            try:
                self.full_clean()
            except ValidationError:
                pass
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.get_role_display()})"
        return f"{self.username} ({self.get_role_display()})"
    
    def is_admin(self):
        return self.role == self.ADMIN
    
    def is_operario(self):
        return self.role == self.OPERARIO
    
    def is_cliente(self):
        return self.role == self.CLIENTE
    
    def has_role(self, *roles):
        return self.role in roles
