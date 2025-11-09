from django.core.management.base import BaseCommand
from orders.models import Warehouse, Product, Inventory
from products.models import Variable
from django.db import transaction

class Command(BaseCommand):
    help = 'Configura datos de prueba: bodegas, productos e inventario inicial'

    def handle(self, *args, **options):
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('Configurando datos de prueba...'))
        self.stdout.write('='*60 + '\n')

        with transaction.atomic():
            # 1. Crear Bodegas
            self.stdout.write(self.style.WARNING('1. Creando bodegas...'))
            warehouses_data = [
                {'name': 'Bodega Norte', 'latitude': 4.710989, 'longitude': -74.072092},
                {'name': 'Bodega Centro', 'latitude': 4.598889, 'longitude': -74.080833},
                {'name': 'Bodega Sur', 'latitude': 4.570868, 'longitude': -74.297333},
            ]
            
            warehouses = []
            for wh_data in warehouses_data:
                wh, created = Warehouse.objects.get_or_create(
                    name=wh_data['name'],
                    defaults={
                        'latitude': wh_data['latitude'],
                        'longitude': wh_data['longitude']
                    }
                )
                status = 'creada' if created else 'ya existia'
                self.stdout.write(f'   - {wh.name}: {status}')
                warehouses.append(wh)

            # 2. Crear Productos (Variables) - Equipos de Protección Personal (EPP)
            self.stdout.write('\n' + self.style.WARNING('2. Creando productos de seguridad...'))
            products_data = [
                'Casco de Seguridad',
                'Guantes Industriales',
                'Gafas de Proteccion',
                'Botas de Seguridad',
                'Chaleco Reflectivo',
                'Mascarilla N95',
                'Protector Auditivo',
                'Arnes de Seguridad',
            ]
            
            variables = []
            for prod_name in products_data:
                # Crear Product (para orders) primero
                product, _ = Product.objects.get_or_create(name=prod_name)
                
                # Crear Variable (para el formulario)
                var, created = Variable.objects.get_or_create(
                    name=prod_name,
                    defaults={'product': product}
                )
                status = 'creado' if created else 'ya existia'
                self.stdout.write(f'   - {var.name}: {status}')
                variables.append(var)

            # 3. Crear Inventario Inicial
            self.stdout.write('\n' + self.style.WARNING('3. Creando inventario inicial...'))
            
            inventory_data = [
                # Casco de Seguridad
                {'product': 'Casco de Seguridad', 'warehouse': 'Bodega Norte', 'quantity': 150},
                {'product': 'Casco de Seguridad', 'warehouse': 'Bodega Centro', 'quantity': 200},
                {'product': 'Casco de Seguridad', 'warehouse': 'Bodega Sur', 'quantity': 100},
                
                # Guantes Industriales
                {'product': 'Guantes Industriales', 'warehouse': 'Bodega Norte', 'quantity': 500},
                {'product': 'Guantes Industriales', 'warehouse': 'Bodega Centro', 'quantity': 400},
                {'product': 'Guantes Industriales', 'warehouse': 'Bodega Sur', 'quantity': 300},
                
                # Gafas de Proteccion
                {'product': 'Gafas de Proteccion', 'warehouse': 'Bodega Norte', 'quantity': 250},
                {'product': 'Gafas de Proteccion', 'warehouse': 'Bodega Centro', 'quantity': 300},
                
                # Botas de Seguridad
                {'product': 'Botas de Seguridad', 'warehouse': 'Bodega Norte', 'quantity': 120},
                {'product': 'Botas de Seguridad', 'warehouse': 'Bodega Sur', 'quantity': 80},
                
                # Chaleco Reflectivo
                {'product': 'Chaleco Reflectivo', 'warehouse': 'Bodega Centro', 'quantity': 350},
                {'product': 'Chaleco Reflectivo', 'warehouse': 'Bodega Sur', 'quantity': 200},
                
                # Mascarilla N95
                {'product': 'Mascarilla N95', 'warehouse': 'Bodega Norte', 'quantity': 1000},
                {'product': 'Mascarilla N95', 'warehouse': 'Bodega Centro', 'quantity': 1500},
                {'product': 'Mascarilla N95', 'warehouse': 'Bodega Sur', 'quantity': 800},
                
                # Protector Auditivo
                {'product': 'Protector Auditivo', 'warehouse': 'Bodega Norte', 'quantity': 180},
                {'product': 'Protector Auditivo', 'warehouse': 'Bodega Centro', 'quantity': 220},
                
                # Arnes de Seguridad
                {'product': 'Arnes de Seguridad', 'warehouse': 'Bodega Norte', 'quantity': 60},
                {'product': 'Arnes de Seguridad', 'warehouse': 'Bodega Centro', 'quantity': 40},
                {'product': 'Arnes de Seguridad', 'warehouse': 'Bodega Sur', 'quantity': 30},
            ]
            
            for inv_data in inventory_data:
                product = Product.objects.get(name=inv_data['product'])
                warehouse = Warehouse.objects.get(name=inv_data['warehouse'])
                
                inv, created = Inventory.objects.get_or_create(
                    product=product,
                    warehouse=warehouse,
                    defaults={'quantity': inv_data['quantity']}
                )
                
                if not created:
                    inv.quantity = inv_data['quantity']
                    inv.save()
                
                self.stdout.write(
                    f'   - {product.name} @ {warehouse.name}: '
                    f'{inv.quantity} unidades'
                )

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('Configuracion completada exitosamente!'))
        self.stdout.write('='*60 + '\n')
        
        self.stdout.write(self.style.SUCCESS('Resumen:'))
        self.stdout.write(f'  - Bodegas creadas: {Warehouse.objects.count()}')
        self.stdout.write(f'  - Productos creados: {Product.objects.count()}')
        self.stdout.write(f'  - Variables creadas: {Variable.objects.count()}')
        self.stdout.write(f'  - Registros de inventario: {Inventory.objects.count()}')
        self.stdout.write(f'  - Stock total: {sum(inv.quantity for inv in Inventory.objects.all())} unidades')

