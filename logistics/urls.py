from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('api/', include('inventory.urls')),
    path('api/', include('products.urls')),
    path('api/', include('orders.urls')),
]
