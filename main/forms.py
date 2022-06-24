from pyexpat import model
from django import forms
from .models import *
from django.core.validators import RegexValidator


class Adicionar_pet(forms.ModelForm):
    class Meta:
        model = Animal
        fields = '__all__'
        labels = {
            'aniversario': 'Aniversário'
        }
        widgets = {
            'aniversario': forms.DateInput(attrs={'data-mask': '00/00/0000'})
        }
    
class Dados(forms.ModelForm):
    class Meta:
        model = User_Dados
        fields = '__all__'
        widgets = {
            'cpf': forms.CharField(validators=[RegexValidator(regex=r'[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}')])
        }
