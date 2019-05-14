from django import forms
from .models import Temperature
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class TemperatureModelForm(forms.ModelForm):

    class Meta:
        model = Temperature
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()