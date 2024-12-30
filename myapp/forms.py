# gas_station/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class GasStationSearchForm(forms.Form):
    address = forms.CharField(label='Enter Address or Location', max_length=255)
    #station_name = forms.CharField(label='Enter Gas Station Name (optional)', max_length=100, required=False)
    station_name = forms.CharField(required=False)
    min_price = forms.DecimalField(label='Minimum Price (optional)', required=False, max_digits=5, decimal_places=2)
    max_price = forms.DecimalField(label='Maximum Price (optional)', required=False, max_digits=5, decimal_places=2)
    min_rating = forms.DecimalField(label='Minimum Rating (optional)', required=False, max_digits=2, decimal_places=1)
    max_rating = forms.DecimalField(label='Maximum Rating (optional)', required=False, max_digits=2, decimal_places=1)






class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']