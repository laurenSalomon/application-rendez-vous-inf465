from django.forms import forms
from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'phone_number']

class OTPVerificationForm(forms.Form):
    code = forms.CharField(max_length=6)