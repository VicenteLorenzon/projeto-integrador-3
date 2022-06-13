from wsgiref.util import request_uri
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpRequest

def index(request):
    return render(request, 'index.html')

def adicionar_pet(request):
    return render(request, 'adicionar_pet.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def carrinho(request):
    return render(request, 'carrinho.html')

def confirmar_servico(request):
    return render(request, 'confirmar_servico.html')

def dados_produto(request):
    return render(request, 'dados_produto.html')

def editar_pet(request):
    return render(request, 'editar_pet.html')

def finalizar_compra(request):
    return render(request, 'finalizar_compra.html')

def login(request):
    return render(request, 'login.html')

def meus_dados(request):
    return render(request, 'meus_dados.html')

def meus_pets(request):
    return render(request, 'meus_pets.html')

def perguntas_frequentes(request):
    return render(request, 'perguntas_frequentes.html')

def produtos(request):
    return render(request, 'produtos.html')

def servicos(request):
    return render(request, 'servicos.html')


    