from django import forms
from .models import House

class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['category', 'location', 'square_meters', 'bedrooms', 'bathrooms', 'price', 'currency']
