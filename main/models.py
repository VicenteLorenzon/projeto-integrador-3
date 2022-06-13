from django.db import models

class Cliente(models.Model):
    cpf = models.CharField(max_length=14)
    sobrenome = models.CharField(max_length=50)

class Cartao(models.Model):
    pass

class Endereco(models.Model):
    pass

class Funcionario(models.Model):
    pass

class Animal(models.Model):
    pass

class Especie(models.Model):
    pass

class Raca(models.Model):
    pass

class Venda(models.Model):
    pass

class Estoque(models.Model):
    pass

class Carrinho(models.Model):
    pass

class Estoque(models.Model):
    pass

class Servico(models.Model):
    pass

class Solicitacao(models.Model):
    pass

class Autorizacao(models.Model):
    pass


