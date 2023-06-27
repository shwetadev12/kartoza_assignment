from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    phone_number = forms.CharField(max_length=12, required=False)
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=True)
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'address', 'phone_number',
            'latitude', 'longitude')
