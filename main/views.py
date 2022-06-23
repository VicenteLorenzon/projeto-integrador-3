from http.client import FORBIDDEN
from imp import reload
from threading import excepthook
from urllib.error import URLError
from wsgiref.util import request_uri
from xmlrpc.client import DateTime
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseRedirect
from .validations import campos_em_branco, senhas_iguais
from django.contrib.auth.models import User
from .models import *
from django.contrib import auth
from django.views.generic.base import RedirectView
from datetime import date

def index(request):
    produtos = Produto.objects.all()
    return render(request, 'index.html', {'produtos': produtos})

def perguntas_frequentes(request):
    return render(request, 'perguntas_frequentes.html')

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

def logout(request):
    auth.logout(request)
    return redirect('index')

def meus_dados(request): #FALTA TUDO
    return render(request, 'meus_dados.html')

def meus_pets(request):
    pets = Animal.objects.filter(user=request.user.id)
    return render(request, 'meus_pets.html', {'pets': pets})

def adicionar_pet(request): #FALTA AJUSTAR TEMPLATE
    if request.method == 'get':
        return render(request, 'adicionar_pet.html')  

    elif request.method == 'post':
        pet = Animal(
            nome = request.POST['nome'].strip(),
            user = request.user,
            especie = Especie.objects.get(id=request.POST['especie']),
            raca = Raca.objects.get(id=request.POST['raca']),
            cor = request.POST['cor'].strip(),
            aniversario = request.POST['aniversario'],
            foto = request.POST['foto']
        )
        pet.save()

def editar_pet(request, id): #FALTA AJUSTAR TEMPLATE
    pet = Animal.objects.get(id=id)
    if request.user != pet.user:
        return HttpResponseForbidden

    elif request.method == 'GET':
        return render(request, 'editar_pet.html', {'pet': pet})

    elif request.method == 'POST':
        pet.nome = request.POST['nome'].strip()
        pet.especie = Especie.objects.get(id=request.POST['especie'])
        pet.raca = Raca.objects.get(id=request.POST['raca'])
        pet.cor = request.POST['cor'].strip()
        pet.aniversario = request.POST['aniversario']
        pet.foto = request.POST['foto']
        pet.save()
        return redirect('meus_pets')

def carrinho(request):
    itens = Carrinho.objects.filter(user=request.user.id)
    return render(request, 'carrinho.html', context={'carrinho': itens})

def mandar_carrinho(request, produto):
    item = Carrinho(user=request.user, produto=Produto.objects.get(id=produto), quantidade=1, valor_unit=Produto.objects.get(id=produto).preco)
    item.save()
    return redirect('carrinho')

def tirar_carrinho(request, item):
    item_carrinho = Carrinho.objects.get(id=item)
    if item_carrinho.user != request.user:
        return HttpResponseForbidden

    item_carrinho.delete()
    return redirect('carrinho')

def finalizar_compra(request):
    carrinho_user = Carrinho.objects.filter(user=request.user.id)
    if request.method == 'get':
        enderecos = Endereco.objects.filter(user=request.user.id)
        preco = 0
        for item in carrinho_user:
            valor_item = item.quantidade * item.valor_unit
            preco += valor_item
        return render(request, 'finalizar_compra.html', context={'contexto':{'enderecos': enderecos, 'preco': preco}})

    elif request.method == 'post':
        forma_entrega = request.POST['forma_entrega']
        endereco = request.POST['endereco']
        for item in carrinho_user:
            venda = Venda(
                user=request.user,
                produto=item.produto,
                data=date.today(),
                endereco=Endereco.objects.get(id=endereco),
                forma_entrega=forma_entrega,
                quantidade=item.quantidade,
                valor_total=(item.quantidade * item.valor_unit)
            )
            venda.save()

        carrinho_user.delete()
        return redirect('index')

def produto(request, id):
    prod = Produto.objects.get(id=id)
    return render(request, 'dados_produto.html', {'produto': prod})

def produtos(request):
    try:
        produtos = Produto.objects.filter(produto__icontains= request.GET['search'])
    except:
        produtos = Produto.objects.all()

    return render(request, 'produtos.html', {'produtos': produtos})

def servicos(request): #FALTA TERMINAR
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