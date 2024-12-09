from django import forms
from .models import Booking
from services.models import Service

class BookingForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',  # Styling checkbox input
        }),
        required=False,
    )
    
    class Meta:
        model = Booking
        fields = ['seats', 'services']
        widgets = {
            'seats': forms.NumberInput(attrs={
                'class': 'form-control',  # Bootstrap class
                'placeholder': 'Enter seats to book',
                'min': 1,
            }),
        }
    
    def clean_seats(self):
        seats = self.cleaned_data.get('seats')
        if seats <= 0:
            raise forms.ValidationError('Jumlah kursi harus lebih dari 0.')
        return seats
