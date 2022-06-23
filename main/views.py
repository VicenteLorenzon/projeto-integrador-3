from http.client import FORBIDDEN
from imp import reload
from threading import excepthook
from urllib.error import URLError
from wsgiref.util import request_uri
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseRedirect
from .validations import campos_em_branco, senhas_iguais
from django.contrib.auth.models import User
from .models import *
from django.contrib import auth
from django.views.generic.base import RedirectView

def index(request):
    produtos = Produto.objects.all()
    return render(request, 'index.html', {'produtos': produtos})

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
            if request.user.is_staff:
                return HttpResponseRedirect('/admin/')
            else:
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
            dados_pessoa = User_Dados.objects.create(user=pessoa, cpf=cpf, telefone=telefone)
            pessoa.save()
            dados_pessoa.save()
            return redirect('login')
    else:
        return render(request, 'cadastro.html')

def carrinho(request):
    itens = Carrinho.objects.filter(user=request.user.id)
    return render(request, 'carrinho.html', context={'carrinho': itens})

def mandar_carrinho(request, produto):
    item = Carrinho(user=request.user, produto=Produto.objects.get(id=produto), quantidade=1, valor_unit=Produto.objects.get(id=produto).preco)
    item.save()
    return redirect('carrinho')

def tirar_carrinho(request, item):
    i = Carrinho.objects.get(id=item).delete()
    return redirect('carrinho')

def confirmar_servico(request):
    return render(request, 'confirmar_servico.html')

def produto(request, id):
    prod = Produto.objects.get(id=id)
    return render(request, 'dados_produto.html', {'produto': prod})

def editar_pet(request, id):
    if request.method == 'GET':
        pet = Animal.objects.get(id=id)
        return render(request, 'editar_pet.html', {'pet': pet})
    elif request.method == 'POST':
        pet = Animal.objects.get(id=id)
        pet.nome = request.POST['nome']
        pet.especie = Especie.objects.get(id=request.POST['especie'])
        pet.raca = Raca.objects.get(id=request.POST['raca'])
        pet.cor = request.POST['cor']
        pet.aniversario = request.POST['aniversario']
        pet.save()
        return redirect('meus_pets')

def finalizar_compra(request):
    return render(request, 'finalizar_compra.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def meus_dados(request):
    return render(request, 'meus_dados.html')

def meus_pets(request):
    pets = Animal.objects.filter(user=request.user.id)
    return render(request, 'meus_pets.html', {'pets': pets})

def perguntas_frequentes(request):
    return render(request, 'perguntas_frequentes.html')

def produtos(request):
    try:
        produtos = Produto.objects.filter(produto__icontains= request.GET['search'])
    except:
        produtos = Produto.objects.all()

    return render(request, 'produtos.html', {'produtos': produtos})

def servicos(request):
    pets = Animal.objects.filter(user=request.user.id)   
    try:
        pet = request.GET['pet']
        if Animal.objects.get(id=pet).user != request.user:
            return HttpResponseForbidden()
        raca = Animal.objects.get(id=pet).raca
        servicos = Servico_Animal_Disponibilidade.objects.filter(raca=raca, disponivel=True)
        return render(request, 'servicos.html', {'contexto':{'pets': pets, 'servicos': servicos, 'nome_pet': 'Serviços disponíves - '+ Animal.objects.get(id=pet).nome}})
    except:
        return render(request, 'servicos.html', {'contexto':{'pets': pets}}) 