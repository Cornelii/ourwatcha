from django import forms
from .models import Role, People


class PeopleModelForm(forms.ModelForm):

    class Meta:
        model = People
        fields = '__all__'


class RoleModelForm(forms.ModelForm):

    class Meta:
        model = Role
        fields = '__all__'


