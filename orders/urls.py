from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('api/inventory/<str:product_name>/', views.inventory_detail, name='inventory_detail'),
    path('api/inventory/<str:product_name>/restock/', csrf_exempt(views.inventory_restock), name='inventory_restock'),
    path('api/orders/<str:product_name>/', csrf_exempt(views.place_order), name='place_order'),
]
