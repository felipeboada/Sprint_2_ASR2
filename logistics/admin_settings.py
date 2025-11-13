# Configuración adicional para mejorar Django Admin

# Títulos personalizados
ADMIN_SITE_HEADER = "PROVESI S.A.S. - Sistema de Gestión"
ADMIN_SITE_TITLE = "PROVESI Admin"
ADMIN_INDEX_TITLE = "Panel de Administración"

# Configuración para mejorar apariencia
ADMIN_REORDER = (
    ('orders', 'Orders'),
    ('authentication', 'Usuarios'),
    ('inventory', 'Inventory'),
    ('products', 'Products'),
)

