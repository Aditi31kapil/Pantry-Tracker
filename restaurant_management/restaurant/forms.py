from django import forms
from .models import Order, Reservation

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table', 'items', 'status']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'name', 'phone', 'reservation_time']
