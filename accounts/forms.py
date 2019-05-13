from django import forms
from .models import Temperature

class TemperatureModelForm(forms.ModelForm):

    class Meta:
        model = Temperature
        fields = '__all__'