from django import forms
from .models import Bus

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['name', 'departure', 'destination', 'departure_time', 'seat', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter bus name'}),
            'departure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter departure location'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter destination'}),
            'departure_time': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local',
                'placeholder': 'Select departure time'
            }),
            'seat': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of seats'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter bus description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'image': forms.TextInput(attrs={'class': 'form-control'}),
        }
