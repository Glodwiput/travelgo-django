from django import forms
from .models import Bus

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['name', 'departure', 'destination', 'departure_time','seat','description', 'price','image']
