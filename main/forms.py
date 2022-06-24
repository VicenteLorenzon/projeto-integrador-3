from pyexpat import model
from django import forms
from .models import *
from .validations import *



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
    
class Dados_form(forms.ModelForm):
    class Meta:
        model = User_Dados
        fields = '__all__'

    def clean(self):
        valida_formato_cpf(self.data.get('cpf'))
        valida_cpf(self.data.get('cpf'))
        super().clean()

class Endereco_form(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'

    def clean(self):
        valida_cep(self.data.get('cep'))
        super().clean()