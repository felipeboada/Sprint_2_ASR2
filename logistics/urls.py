from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    # Autenticación
    path('', include('authentication.urls')),
    # Rutas de las aplicaciones
    path('', include('inventory.urls')),
    path('', include('products.urls')),
    # Rutas de API REST
    path('api/', include('orders.urls')),
]
