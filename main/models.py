from django.db import models
from django.contrib.auth.models import User

class User_Dados(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=15)
    osbervacao = models.TextField(max_length=200)
    foto = models.ImageField()

class Cartao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=25)
    sobrenome = models.CharField(max_length=25)
    numero = models.CharField(max_length=19)
    validade = models.DateField()
    cvv = models.PositiveSmallIntegerField()

class Endereco(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cep = models.CharField(max_length=14)
    rua = models.CharField(max_length=75)
    complemento = models.CharField(max_length=75)
    numero = models.PositiveSmallIntegerField()
    
class Especie(models.Model):
    especie = models.CharField(max_length=30)

class Raca(models.Model):
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    raca = models.CharField(max_length=30)

class Animal(models.Model):
    nome = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE)
    cor = models.CharField(max_length=30)
    aniversario = models.DateField()
    foto = models.ImageField()

class Produto(models.Model):
    produto = models.CharField(max_length=75)
    preco = models.DecimalField(decimal_places=2, max_digits=12)
    estoque = models.IntegerField()

class Carrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    valor_unit = models.DecimalField(decimal_places=2, max_digits=12)

class Servico(models.Model):
    servico = models.CharField(max_length=75)
    preco = models.DecimalField(decimal_places=2, max_digits=12)

class Solicitacao(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    data = models.DateTimeField()
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    forma_entrada = models.CharField(max_length=1)
    forma_saida = models.CharField(max_length=1)
    valor = models.DecimalField(decimal_places=2, max_digits=12)

class Venda(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    data = models.DateTimeField()
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    forma_entrega = models.CharField(max_length=1)
    quantidade = models.IntegerField()
    valor_total = models.DecimalField(decimal_places=2, max_digits=12)

class Servico_Animal_Disponibilidade(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE)
    disponivel = models.BooleanField()