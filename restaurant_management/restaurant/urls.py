from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('order/', views.order, name='order'),
    path('reservations/', views.reservations, name='reservations'),
    path('inventory/', views.inventory, name='inventory'),
]
