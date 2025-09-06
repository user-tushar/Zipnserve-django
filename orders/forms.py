from django import forms
from . models import Order

class  OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address1', 'address2', 'country', 'state', 'city', 'pin', 'order_note']