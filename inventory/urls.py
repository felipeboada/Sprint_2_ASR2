from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('stock/', views.measurement_list),
    path('stockcreate/', csrf_exempt(views.measurement_create), name='stockCreate'),
    path('ordercreate/', csrf_exempt(views.measurement_order_create), name='orderCreate'),
]