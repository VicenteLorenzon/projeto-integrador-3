from django.db import models
from django.contrib.auth.models import User

class User_Dados(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=15)
    osbervacao = models.TextField(max_length=200)
    class Meta:
        verbose_name = _("Dados de usuário")
        verbose_name_plural = _("Dados dos usuários")
    def __str__(self):
        usuario = User.objects.get(id=self.user)
        return str(self.user) ' - ' + usuario.first_name + ' ' + usuario.last_name

class Cartao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=25)
    sobrenome = models.CharField(max_length=25)
    numero = models.CharField(max_length=19)
    validade = models.DateField()
    cvv = models.PositiveSmallIntegerField()
    class Meta:
        verbose_name = _("Cartão")
        verbose_name_plural = _("Cartões")
    def __str__(self):
        return self.numero

class Endereco(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cep = models.CharField(max_length=14)
    rua = models.CharField(max_length=75)
    complemento = models.CharField(max_length=75)
    numero = models.PositiveSmallIntegerField()
    class Meta:
        verbose_name = _("Endereço")
        verbose_name_plural = _("Endereços")
    def __str__(self):
        return self.rua + ' ' + str(self.numero)
    
class Especie(models.Model):
    especie = models.CharField(max_length=30)
    class Meta:
        verbose_name = _("Espécie")
        verbose_name_plural = _("Espécies")
    def __str__(self):
        return self.especie

class Raca(models.Model):
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    raca = models.CharField(max_length=30)
    class Meta:
        verbose_name = _("Raça")
        verbose_name_plural = _("Raças")
    def __str__(self):
        return self.raca

class Animal(models.Model):
    nome = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE)
    cor = models.CharField(max_length=30)
    aniversario = models.DateField()
    foto = models.ImageField(upload_to='pets')
    class Meta:
        verbose_name = _("Animal")
        verbose_name_plural = _("Animais")
    def __str__(self):
        usuario = User.objects.get(id=self.user)
        return self.nome + ' - ' + usuario.first_name + ' ' + usuario.last_name

class Produto(models.Model):
    produto = models.CharField(max_length=75)
    preco = models.DecimalField(decimal_places=2, max_digits=12)
    estoque = models.IntegerField()
    foto = models.ImageField(upload_to='produtos')
    class Meta:
        verbose_name = _("Produto")
        verbose_name_plural = _("Produtos")
    def __str__(self):
        return self.produto

class Carrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    valor_unit = models.DecimalField(decimal_places=2, max_digits=12)
    class Meta:
        verbose_name = _("Carrinho")
        verbose_name_plural = _("Carrinhos")
    def __str__(self):
        usuario = User.objects.get(id=self.user)
        return usuario.first_name + ' ' + usuario.last_name + ' - ' + Produto.objects.get(id=self.produto).produto

class Servico(models.Model):
    servico = models.CharField(max_length=75)
    preco = models.DecimalField(decimal_places=2, max_digits=12)
    foto = models.ImageField(upload_to='servicos')
    class Meta:
        verbose_name = _("Serviço")
        verbose_name_plural = _("Serviços")
    def __str__(self):
        return self.servico

class Solicitacao(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    horario = models.DateTimeField()
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    forma_entrada = models.CharField(max_length=1, choices=[('P', 'Buscar no endereço'), ('C', 'Cliente leva')])
    forma_saida = models.CharField(max_length=1, choices=[('P', 'Levar ao cliente'), ('C', 'Cliente busca')])
    valor = models.DecimalField(decimal_places=2, max_digits=12)
    status = models.CharField(max_length=1, choices=[('A', 'Ainda não iniciado'), 
                                                     ('B', 'Em andamento no pet shop'), 
                                                     ('C', 'Concluído, pet já em casa'), 
                                                     ('D', 'Concluído, aguardando retirada do pet')])
    class Meta:
        verbose_name = _("Solicitação")
        verbose_name_plural = _("Solicitações")
    def __str__(self):
        return self.animal + ' - ' + self.servico + ' - ' + str(self.data)

class Venda(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    data = models.DateTimeField()
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    forma_entrega = models.CharField(max_length=1, choices=[('P', 'Delivery'), ('C', 'Retirada')])
    quantidade = models.IntegerField()
    valor_total = models.DecimalField(decimal_places=2, max_digits=12)
    class Meta:
        verbose_name = _("Venda")
        verbose_name_plural = _("Vendas")
    def __str__(self):
        return self.user + ' - ' + self.produto + ' - ' + str(self.data)

class Servico_Animal_Disponibilidade(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE)
    disponivel = models.BooleanField()
    class Meta:
        verbose_name = _("Disponibilidade de serviço")
        verbose_name_plural = _("Disponibilidades de serviço")
    def __str__(self):
        return 'Aut. ' + Servico.objects.get(id=self.servico).servico + ' - ' + Raca.objects.get(id=self.raca).raca
