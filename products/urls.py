from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('productos/', views.variable_list, name='productosList'),
    path('productocreate/', csrf_exempt(views.variable_create), name='productoCreate'),
]