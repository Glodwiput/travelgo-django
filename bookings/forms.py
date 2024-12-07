from django import forms
from .models import Booking
from services.models import Service

class BookingForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Booking
        fields = ['seats', 'services']
    
    def clean_seats(self):
        seats = self.cleaned_data.get('seats')
        if seats <= 0:
            raise forms.ValidationError('Jumlah kursi harus lebih dari 0.')
        return seats
