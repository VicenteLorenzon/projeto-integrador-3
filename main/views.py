from wsgiref.util import request_uri
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .validations import senhas_iguais
from django.contrib.auth.models import User
from .models import Cliente, User
from django.contrib import auth

def index(request):
    return render(request, 'index.html')

def adicionar_pet(request):
    return render(request, 'adicionar_pet.html')

def cadastro(request):
    if request.method == 'POST':
        mensagens_erro = []
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        email = request.POST['email']
        cpf = request.POST['cpf']
        telefone = request.POST['telefone']
        senha = request.POST['senha']
        senha2 = request.POST['senha2']

        senhas_iguais(senha, senha2, mensagens_erro)
        if(len(mensagens_erro) > 0):
            return render(request, 'cadastro.html', {'erros': mensagens_erro})
        else:
            pessoa = User.objects.create_user(username=email, first_name=nome, last_name=sobrenome, email=email, password=senha)
            dados_pessoa = Cliente.objects.create(user=pessoa, cpf=cpf, telefone=telefone)
            pessoa.save()
            dados_pessoa.save()
            return redirect('login')
    else:
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
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        user = auth.authenticate(request, username=email, password=senha)
        if user is not None:
            auth.login(request, user)
            return redirect('meus_dados')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

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


    