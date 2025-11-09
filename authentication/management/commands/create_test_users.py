from django.core.management.base import BaseCommand
from authentication.models import User

class Command(BaseCommand):
    help = 'Crea usuarios de prueba para cada rol del sistema'

    def handle(self, *args, **options):
        users_to_create = [
            {
                'username': 'admin',
                'email': 'admin@logistica.com',
                'password': 'admin123',
                'role': User.ADMIN,
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'operario',
                'email': 'operario@logistica.com',
                'password': 'operario123',
                'role': User.OPERARIO,
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'phone': '3001234567',
            },
            {
                'username': 'cliente',
                'email': 'cliente@logistica.com',
                'password': 'cliente123',
                'role': User.CLIENTE,
                'first_name': 'María',
                'last_name': 'García',
                'phone': '3009876543',
                'address': 'Calle 123 #45-67, Bogotá',
            },
        ]

        created_count = 0
        skipped_count = 0

        for user_data in users_to_create:
            username = user_data['username']
            
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Usuario "{username}" ya existe, saltando...')
                )
                skipped_count += 1
                continue
            
            password = user_data.pop('password')
            user = User.objects.create_user(**user_data)
            user.set_password(password)
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'[OK] Usuario "{username}" creado exitosamente '
                    f'({user.get_role_display()})'
                )
            )
            created_count += 1

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'Proceso completado:'))
        self.stdout.write(f'  - Usuarios creados: {created_count}')
        self.stdout.write(f'  - Usuarios existentes: {skipped_count}')
        self.stdout.write('='*60)
        
        if created_count > 0:
            self.stdout.write('\n' + self.style.SUCCESS('Credenciales de acceso:'))
            self.stdout.write('  - Admin:    usuario="admin"    contrasena="admin123"')
            self.stdout.write('  - Operario: usuario="operario" contrasena="operario123"')
            self.stdout.write('  - Cliente:  usuario="cliente"  contrasena="cliente123"')

