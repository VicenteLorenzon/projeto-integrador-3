from pyexpat import model
from django import forms
from .models import Animal

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
