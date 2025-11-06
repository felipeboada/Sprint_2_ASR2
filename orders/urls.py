from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('inventory/<str:product_name>/', views.inventory_detail, name='inventory_detail'),
    path('inventory/<str:product_name>/restock/', csrf_exempt(views.inventory_restock), name='inventory_restock'),
    path('orders/<str:product_name>/', csrf_exempt(views.place_order), name='place_order'),
    path("auto_order/", views.create_order_view, name="auto_order"),
]
