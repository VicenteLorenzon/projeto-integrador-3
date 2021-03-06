from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adicionar_pet/', views.adicionar_pet, name='adicionar_pet'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('mandar_carrinho/<int:produto>', views.mandar_carrinho, name='mandar_carrinho'),
    path('tirar_carrinho/<int:item>', views.tirar_carrinho, name='tirar_carrinho'),
    path('produto/<int:id>', views.produto, name='produto'),
    path('editar_pet/<int:id>', views.editar_pet, name='editar_pet'),
    path('finalizar_compra/', views.finalizar_compra, name='finalizar_compra'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('meus_dados/', views.meus_dados, name='meus_dados'),
    path('meus_pets/', views.meus_pets, name='meus_pets'),
    path('minhas_solicitacoes/', views.minhas_solicitacoes, name='minhas_solicitacoes'),
    path('perguntas_frequentes/', views.perguntas_frequentes, name='perguntas_frequentes'),
    path('produtos/', views.produtos, name='produtos'),
    path('servicos/', views.servicos, name='servicos'),
    path('adicionar_endereco/', views.adicionar_endereco, name='adicionar_endereco'), 
    path('editar_dados/', views.editar_dados, name='editar_dados'),
    path('excluir_endereco/<int:id>', views.excluir_endereco, name='excluir_endereco'),
]
