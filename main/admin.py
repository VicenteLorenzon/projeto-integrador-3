from django.contrib import admin
from .models import *
from .forms import Adicionar_pet

class User_Dados_admin(admin.ModelAdmin):
    list_display = ('user', 'cpf', 'telefone', )
    list_display_links = ('user', 'cpf', 'telefone', )

class Cartao_admin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'nome', 'sobrenome')
    list_display_links = ('id', )

class Endereco_admin(admin.ModelAdmin):
    list_display = ('id', 'rua', 'numero', 'cep', )
    list_display_links = ('id', )

class Especie_admin(admin.ModelAdmin):
    list_display = ('id', 'especie', )
    list_display_links = ('id', 'especie', )

class Raca_admin(admin.ModelAdmin):
    list_display = ('id', 'raca', 'especie', )
    list_display_links = ('id', 'raca', )

class Animal_admin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'user', 'especie', 'raca', )
    list_display_links = ('id', 'nome', )
    search_fields = ('nome', )
    list_filter = ('especie', 'raca', 'user', )

class Produto_admin(admin.ModelAdmin):
    list_display = ('id', 'produto', 'preco', 'estoque', )
    list_display_links = ('id', 'produto', )
    search_fields = ('produto', )

class Servico_admin(admin.ModelAdmin):
    list_display = ('id', 'servico', 'preco', )
    list_display_links = ('id', 'servico', )
    search_fields = ('servico', )

class Solicitacao_admin(admin.ModelAdmin):
    list_display = ('id', 'animal', 'servico', 'status')
    list_display_links = ('id', 'animal', 'servico', )
    search_fields = ('animal', 'servico', )

class Venda_admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'produto', 'data', )
    list_display_links = ('id', 'user', 'produto', )
    search_fields = ('user', 'produto', )

class Servico_Animal_Disponibilidade_admin(admin.ModelAdmin):
    list_display = ('id', 'raca', 'servico', 'disponivel', )
    list_display_links = ('id', 'raca', 'servico', )
    search_fields = ('raca', 'servico', )

admin.site.register(User_Dados, User_Dados_admin)
admin.site.register(Cartao, Cartao_admin)
admin.site.register(Endereco, Endereco_admin)
admin.site.register(Especie, Especie_admin)
admin.site.register(Raca, Raca_admin)
admin.site.register(Animal, Animal_admin)
admin.site.register(Produto, Produto_admin)
admin.site.register(Servico, Servico_admin)
admin.site.register(Solicitacao, Solicitacao_admin)
admin.site.register(Venda, Venda_admin)
admin.site.register(Servico_Animal_Disponibilidade, Servico_Animal_Disponibilidade_admin)
