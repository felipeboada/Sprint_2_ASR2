from django.contrib import admin
from django.urls import include, path
from . import views

# Personalización del Django Admin
admin.site.site_header = "PROVESI S.A.S. - Sistema de Gestión"
admin.site.site_title = "PROVESI Admin"
admin.site.index_title = "Panel de Administración"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('', include('authentication.urls')),
    path('', include('inventory.urls')),
    path('', include('products.urls')),
    path('api/', include('orders.urls')),
]
