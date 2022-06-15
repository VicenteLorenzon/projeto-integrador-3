from django.contrib import admin
from .models import *
from .forms import Adicionar_pet

class Animal_admin(admin.ModelAdmin):
    form = Adicionar_pet

admin.site.register(Cliente)
admin.site.register(Cartao)
admin.site.register(Endereco)
admin.site.register(Funcionario)
admin.site.register(Especie)
admin.site.register(Raca)
admin.site.register(Animal, Animal_admin)
admin.site.register(Produto)
admin.site.register(Servico)
admin.site.register(Solicitacao)
admin.site.register(Venda)
admin.site.register(Autorizacao)
