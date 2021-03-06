from http.client import FORBIDDEN
from imp import reload
from threading import excepthook
from urllib.error import URLError
from wsgiref.util import request_uri
from xmlrpc.client import DateTime
from django.forms import ValidationError
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseRedirect
from .validations import *
from django.contrib.auth.models import User
from .models import *
from django.contrib import auth
from django.views.generic.base import RedirectView
from datetime import date
import os

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
            mensagens_erro.append('E-mail e senha n??o combinam')
        return render(request, 'login.html', {'erros': mensagens_erro})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def excluir_endereco(request, id):
    if request.user != Endereco.objects.get(pk=id).user:
        return HttpResponseForbidden
    Endereco.objects.get(pk=id).delete()
    return redirect('meus_dados')

def adicionar_endereco(request):
    if request.method == 'POST':
        mensagens_erro = []
        cep = request.POST['cep'].strip()
        cidade = request.POST['cidade'].strip()
        rua = request.POST['rua'].strip()
        complemento = request.POST['complemento'].strip()
        numero = request.POST['numero'].strip()

        campos_em_branco([cep, cidade, rua, complemento, numero], mensagens_erro)
        valida_cep_normal(cep, mensagens_erro)
        if(len(mensagens_erro) > 0):
            return redirect('meus_dados')
        else:
            endereco = Endereco(
                user = request.user,
                cep=cep, 
                rua=rua, 
                complemento=complemento, 
                numero=numero)
            endereco.save()
            return redirect('meus_dados')

def editar_dados(request):
    if request.method == 'POST':
        mensagens_erro = []
        nome = request.POST['nome'].strip()
        sobrenome = request.POST['sobrenome'].strip()
        email = request.POST['email'].strip()
        cpf = request.POST['cpf'].strip()
        telefone = request.POST['telefone'].strip()

        campos_em_branco([nome, sobrenome, email, cpf, telefone], mensagens_erro)
        valida_cpf_normal(cpf, mensagens_erro)
        if(len(mensagens_erro) > 0):
            return redirect('meus_dados')
        else:
            user = request.user
            dados = User_Dados.objects.get(pk=request.user.id)
            dados.cpf = cpf
            dados.telefone = telefone
            user.first_name = nome
            user.last_name = sobrenome
            user.username = email
            user.email = email

            user.save()
            dados.save()
            return redirect('meus_dados')

def meus_dados(request):
    return render(request, 'meus_dados.html', context={
        'contexto': {
            'enderecos': Endereco.objects.filter(user=request.user),
            'user':request.user,
            'dados':User_Dados.objects.get(pk=request.user.id)
        }
    })

def meus_pets(request):
    pets = Animal.objects.filter(user=request.user.id)
    return render(request, 'meus_pets.html', {'pets': pets})

def minhas_solicitacoes(request):
    solicitacoes = Solicitacao.objects.filter(animal__in = Animal.objects.filter(user=request.user))
    return render(request, 'minhas_solicitacoes.html', context={'solicitacoes': solicitacoes}) 

def adicionar_pet(request):
    if request.method == 'GET':
        racas = Raca.objects.all()
        return render(request, 'adicionar_pet.html', context={'contexto':{'racas': racas}})  

    elif request.method == 'POST':
        erros = []
        nome = request.POST['nome'].strip(),
        user = request.user,
        raca = Raca.objects.get(id=request.POST['raca']),
        cor = request.POST['cor'].strip(),
        aniversario = request.POST['aniversario'],
        try:
            foto = request.FILES['foto']
        except: foto = ''
        campos_em_branco([nome, user, raca, cor, aniversario, foto], erros)
        if len(erros) == 0:
            pet = Animal(
                nome = request.POST['nome'].strip(),
                user = request.user,
                raca = Raca.objects.get(id=request.POST['raca']),
                cor = request.POST['cor'].strip(),
                aniversario = request.POST['aniversario'],
                foto = foto
            )
            pet.save()
            return redirect('meus_pets')
        else:
            racas = Raca.objects.all()
            return render(request, 'adicionar_pet.html', context={'contexto':{'racas': racas, 'erros': erros}})

def editar_pet(request, id):
    pet = Animal.objects.get(id=id)
    if request.user != pet.user:
        return HttpResponseForbidden

    elif request.method == 'GET':
        racas = Raca.objects.all()
        return render(request, 'editar_pet.html', context={'contexto':{'racas': racas, 'pet': pet}})

    elif request.method == 'POST':
        pet.nome = request.POST['nome'].strip()
        pet.raca = Raca.objects.get(id=request.POST['raca'])
        pet.cor = request.POST['cor'].strip()
        pet.aniversario = request.POST['aniversario']
        try:
            pet.foto = request.FILES['foto']
        except:
            pass
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
    if len(carrinho_user) == 0:
        return HttpResponseForbidden
    if request.method == 'GET':
        enderecos = Endereco.objects.filter(user=request.user.id)
        preco = 0
        for item in carrinho_user:
            valor_item = item.quantidade * item.valor_unit
            preco += valor_item
        return render(request, 'finalizar_compra.html', context={'contexto':{'enderecos': enderecos, 'preco': preco}})

    elif request.method == 'POST':
        forma_entrega = request.POST['forma_entrega']
        endereco = request.POST['endereco']
        for item in carrinho_user:
            produto = item.produto
            venda = Venda(
                user=request.user,
                produto=produto,
                data=date.today(),
                endereco=Endereco.objects.get(id=endereco),
                forma_entrega=forma_entrega,
                quantidade=item.quantidade,
                valor_total=(item.quantidade * item.valor_unit)
            )
            produto.estoque = produto.estoque - item.quantidade
            produto.save()
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

def servicos(request):
    enderecos = Endereco.objects.filter(user=request.user.id)
    pets = Animal.objects.filter(user=request.user.id)
    if request.method == 'GET':
        try:
            pet = request.GET['pet']
            if Animal.objects.get(id=pet).user != request.user:
                return HttpResponseForbidden()
            raca = Animal.objects.get(id=pet).raca
            servicos = Servico_Animal_Disponibilidade.objects.filter(raca=raca, disponivel=True)
            print(servicos)
            return render(request, 'servicos.html', {
                'contexto':{
                    'pets': pets, 
                    'enderecos': enderecos, 
                    'servicos': servicos, 
                    'pet': Animal.objects.get(id=pet)
                }
            })
            
        except:
            return render(request, 'servicos.html', {'contexto':{'pets': pets}})

    elif request.method == 'POST':
        erros = []
        servicos_selecionados = []
        for item, valor in request.POST.items():
                if(item.find('serv') != -1):
                    servicos_selecionados.append(int(item.split('serv')[1]))
                    print(servicos_selecionados)
        if len(servicos_selecionados) == 0:
            erros.append('Voc?? deve selecionar pelo menos um servi??o')
        pet = request.POST['pet']
        horario = request.POST['agenda']
        forma_entrada = request.POST['forma_entrada']
        forma_saida = request.POST['forma_saida']
        endereco = request.POST['endereco']        

        if len(erros) > 0:
            return render(request, 'servicos.html', {'contexto':{'pets': pets, 'erros': erros}})
        else:
            for servico in servicos_selecionados: 
                solicitacao = 0
                if(not (forma_entrada == 'C' and forma_saida == 'C')): 
                    solicitacao = Solicitacao(
                        animal = Animal.objects.get(id=request.POST['pet']),
                        horario = horario,
                        servico = Servico.objects.get(id=servico),
                        endereco = Endereco.objects.get(id=endereco),
                        forma_entrada = forma_entrada,
                        forma_saida = forma_saida,
                        valor = Servico.objects.get(id=servico).preco,
                        status = 'A'
                    )
                else:
                    solicitacao = Solicitacao(
                        animal = Animal.objects.get(id=request.POST['pet']),
                        horario = horario,
                        servico = Servico.objects.get(id=servico),
                        endereco = None,
                        forma_entrada = forma_entrada,
                        forma_saida = forma_saida,
                        valor = Servico.objects.get(id=servico).preco,
                        status = 'A' 
                    ) 
                solicitacao.save() 
            return redirect('index')     
        
