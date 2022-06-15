from imp import reload
from wsgiref.util import request_uri
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .validations import campos_em_branco, senhas_iguais
from django.contrib.auth.models import User
from .models import Cliente, User, Produto
from django.contrib import auth

def index(request):
    return render(request, 'index.html')

def adicionar_pet(request):
    return render(request, 'adicionar_pet.html')

def login(request):
    if request.method == 'POST':
        mensagens_erro = []
        email = request.POST['email']
        senha = request.POST['senha']
        user = auth.authenticate(request, username=email, password=senha)

        campos_em_branco([email, senha], mensagens_erro)

        if user is not None:
            auth.login(request, user)
            return redirect('meus_dados')
        else:
            mensagens_erro.append('E-mail e senha não combinam')
        return render(request, 'login.html', {'erros': mensagens_erro})
    else:
        return render(request, 'login.html')

def cadastro(request):
    if request.method == 'POST':
        mensagens_erro = []
        nome = request.POST['nome'].strip()
        sobrenome = request.POST['sobrenome'].strip()
        email = request.POST['email'].strip()
        cpf = request.POST['cpf'].strip()
        telefone = request.POST['telefone'].strip()
        senha = request.POST['senha']
        senha2 = request.POST['senha2']

        campos_em_branco([nome, sobrenome, email, cpf, telefone, senha, senha2], mensagens_erro)
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
    try:
        produtos = Produto.objects.filter(produto__icontains= request.GET['search'])
    except:
        produtos = Produto.objects.all()
        
    return render(request, 'produtos.html', {'produtos': produtos})

def servicos(request):
    return render(request, 'servicos.html')


    