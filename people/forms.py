from django import forms
from .models import Role, Director, Actor, Staff


class DirectorModelForm(forms.ModelForm):

    class Meta:
        model = Director
        fields = '__all__'

class ActorModelForm(forms.ModelForm):

    class Meta:
        model = Actor
        fields = '__all__'

class StaffModelForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = '__all__'

class RoleModelForm(forms.ModelForm):

    class Meta:
        model = Role
        fields = '__all__'


