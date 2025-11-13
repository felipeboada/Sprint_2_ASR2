from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .validators import (
    validate_coordinates, validate_name_format, validate_positive_quantity,
    validate_non_negative, product_name_validator, validate_phone_number,
    validate_nit, validate_address_format
)


class Warehouse(models.Model):
    name = models.CharField(max_length=100, unique=True, validators=[validate_name_format])
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True, null=True, validators=[validate_address_format])
    phone = models.CharField(max_length=20, blank=True, null=True, validators=[validate_phone_number])
    capacity = models.PositiveIntegerField(default=50000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
        ordering = ['name']
        indexes = [models.Index(fields=['name']), models.Index(fields=['is_active'])]
    
    def clean(self):
        errors = {}
        if self.name:
            self.name = self.name.strip()
            if not self.name:
                errors['name'] = 'El nombre no puede estar vacío'
            if Warehouse.objects.filter(name__iexact=self.name).exclude(pk=self.pk).exists():
                errors['name'] = 'Ya existe una bodega con este nombre'
        
        if self.latitude is not None and self.longitude is not None:
            try:
                validate_coordinates(self.latitude, self.longitude)
            except ValidationError as e:
                errors['latitude'] = e.message
        else:
            if self.latitude is None:
                errors['latitude'] = 'La latitud es obligatoria'
            if self.longitude is None:
                errors['longitude'] = 'La longitud es obligatoria'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        if not kwargs.pop('skip_validation', False):
            self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_current_stock(self):
        return self.inventories.aggregate(total=models.Sum('quantity'))['total'] or 0
    
    def get_available_capacity(self):
        return self.capacity - self.get_current_stock()


class Supplier(models.Model):
    name = models.CharField(max_length=150, unique=True, validators=[validate_name_format])
    nit = models.CharField(max_length=12, unique=True, validators=[validate_nit])
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, validators=[validate_phone_number])
    address = models.TextField(validators=[validate_address_format])
    city = models.CharField(max_length=100, validators=[validate_name_format])
    contact_person = models.CharField(max_length=150, validators=[validate_name_format])
    is_active = models.BooleanField(default=True)
    credit_days = models.PositiveIntegerField(default=30)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']), models.Index(fields=['nit']),
            models.Index(fields=['email']), models.Index(fields=['is_active'])
        ]
    
    def clean(self):
        errors = {}
        if self.name:
            self.name = self.name.strip()
            if not self.name:
                errors['name'] = 'El nombre no puede estar vacío'
            if Supplier.objects.filter(name__iexact=self.name).exclude(pk=self.pk).exists():
                errors['name'] = 'Ya existe un proveedor con este nombre'
        
        if self.nit:
            self.nit = self.nit.strip()
            if Supplier.objects.filter(nit=self.nit).exclude(pk=self.pk).exists():
                errors['nit'] = 'Ya existe un proveedor con este NIT'
        
        if self.email:
            self.email = self.email.lower().strip()
            if Supplier.objects.filter(email__iexact=self.email).exclude(pk=self.pk).exists():
                errors['email'] = 'Ya existe un proveedor con este email'
        
        if self.rating is not None and (self.rating < 0 or self.rating > 5):
            errors['rating'] = 'La calificación debe estar entre 0 y 5'
        
        if self.credit_days and self.credit_days > 365:
            errors['credit_days'] = 'Los días de crédito no pueden exceder 365'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        if not kwargs.pop('skip_validation', False):
            self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.nit})"


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, validators=[product_name_validator])
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='products', null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[validate_non_negative])
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[validate_non_negative])
    category = models.CharField(max_length=100, blank=True, null=True)
    min_stock = models.PositiveIntegerField(default=0)
    max_stock = models.PositiveIntegerField(default=10000)
    is_active = models.BooleanField(default=True)
    requires_special_handling = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']), models.Index(fields=['sku']),
            models.Index(fields=['category']), models.Index(fields=['is_active'])
        ]
    
    def clean(self):
        errors = {}
        if self.name:
            self.name = self.name.strip()
            if not self.name:
                errors['name'] = 'El nombre no puede estar vacío'
            if Product.objects.filter(name__iexact=self.name).exclude(pk=self.pk).exists():
                errors['name'] = 'Ya existe un producto con este nombre'
        
        if self.sku:
            self.sku = self.sku.strip().upper()
            if Product.objects.filter(sku__iexact=self.sku).exclude(pk=self.pk).exists():
                errors['sku'] = 'Ya existe un producto con este SKU'
        
        if self.unit_price and self.cost_price and self.unit_price < self.cost_price:
            errors['unit_price'] = 'El precio de venta no puede ser menor al precio de costo'
        
        if self.min_stock and self.max_stock and self.min_stock > self.max_stock:
            errors['min_stock'] = 'El stock mínimo no puede ser mayor al stock máximo'
        
        if self.supplier and not self.supplier.is_active:
            errors['supplier'] = f'El proveedor {self.supplier.name} no está activo'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        if not kwargs.pop('skip_validation', False):
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_total_stock(self):
        return self.inventories.aggregate(total=models.Sum('quantity'))['total'] or 0
    
    def get_profit_margin(self):
        if self.cost_price and self.cost_price > 0:
            return ((self.unit_price - self.cost_price) / self.cost_price) * 100
        return 0


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventories', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    last_restock_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        unique_together = [('product', 'warehouse')]
        indexes = [
            models.Index(fields=['product', 'quantity']),
            models.Index(fields=['warehouse']),
            models.Index(fields=['product', 'warehouse'])
        ]
    
    def clean(self):
        errors = {}
        if not self.product:
            errors['product'] = 'El producto es obligatorio'
        if not self.warehouse:
            errors['warehouse'] = 'La bodega es obligatoria'
        
        if self.product and not self.product.is_active:
            errors['product'] = f'El producto {self.product.name} no está activo'
        
        if self.warehouse and not self.warehouse.is_active:
            errors['warehouse'] = f'La bodega {self.warehouse.name} no está activa'
        
        if self.reserved_quantity and self.quantity and self.reserved_quantity > self.quantity:
            errors['reserved_quantity'] = 'La cantidad reservada no puede exceder la cantidad disponible'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        if not kwargs.pop('skip_validation', False):
            self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        wn = self.warehouse.name if self.warehouse else "N/A"
        return f"{self.product.name} @ {wn} — {self.quantity} u"
    
    def get_available_quantity(self):
        return self.quantity - self.reserved_quantity


class Order(models.Model):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    REJECTED = 'REJECTED'
    CANCELLED = 'CANCELLED'
    IN_TRANSIT = 'IN_TRANSIT'
    DELIVERED = 'DELIVERED'

    STATUS_CHOICES = [
        (PENDING, 'Pendiente'), (CONFIRMED, 'Confirmado'), (REJECTED, 'Rechazado'),
        (CANCELLED, 'Cancelado'), (IN_TRANSIT, 'En Tránsito'), (DELIVERED, 'Entregado'),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orders')
    units = models.PositiveIntegerField(validators=[validate_positive_quantity])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    assigned_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, null=True, blank=True, related_name='orders')
    customer = models.ForeignKey('authentication.User', on_delete=models.PROTECT, null=True, blank=True, related_name='orders')
    delivery_address = models.TextField(blank=True, null=True, validators=[validate_address_format])
    delivery_zone = models.CharField(max_length=50, blank=True, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', 'status']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['customer']),
            models.Index(fields=['assigned_warehouse'])
        ]
    
    def clean(self):
        errors = {}
        if not self.product:
            errors['product'] = 'El producto es obligatorio'
        
        if self.product and not self.product.is_active:
            errors['product'] = f'El producto {self.product.name} no está activo'
        
        if not self.units or self.units <= 0:
            errors['units'] = 'La cantidad debe ser mayor a cero'
        if self.units and self.units > 10000:
            errors['units'] = 'La cantidad máxima por pedido es 10,000 unidades'
        
        if self.assigned_warehouse:
            if not self.assigned_warehouse.is_active:
                errors['assigned_warehouse'] = f'La bodega {self.assigned_warehouse.name} no está activa'
            
            if self.status == self.CONFIRMED:
                try:
                    inventory = Inventory.objects.get(product=self.product, warehouse=self.assigned_warehouse)
                    if not inventory.get_available_quantity() >= self.units:
                        errors['units'] = f'Stock insuficiente. Disponible: {inventory.get_available_quantity()}'
                except Inventory.DoesNotExist:
                    errors['assigned_warehouse'] = f'No hay inventario del producto en esta bodega'
        
        if self.product and self.units:
            expected_total = self.product.unit_price * self.units
            if self.total_price and abs(self.total_price - expected_total) > 0.01:
                self.total_price = expected_total
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        from django.utils import timezone
        if self.pk:
            old_order = Order.objects.get(pk=self.pk)
            if old_order.status != self.status:
                if self.status == self.CONFIRMED and not self.confirmed_at:
                    self.confirmed_at = timezone.now()
                elif self.status == self.DELIVERED and not self.delivered_at:
                    self.delivered_at = timezone.now()
        
        if not kwargs.pop('skip_validation', False):
            self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.product.name} x{self.units} [{self.get_status_display()}]"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Order)
def update_inventory_on_confirm(sender, instance, **kwargs):
    if instance.status == Order.CONFIRMED:
        try:
            inventory = Inventory.objects.get(product=instance.product, warehouse=instance.assigned_warehouse)
            inventory.quantity = max(inventory.quantity - instance.units, 0)
            inventory.save()
        except Inventory.DoesNotExist:
            pass

