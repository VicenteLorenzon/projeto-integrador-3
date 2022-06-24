import re
from django.forms import ValidationError

def senhas_iguais(senha, senha2, lista):
    if(senha != senha2):
        lista.append('As senhas não combinam')

def campos_em_branco(campos, lista):
    branco = False
    for campo in campos:
        if campo == '':
            branco = True
            break
    if branco:
        lista.append('Preencha todos os campos!')

#VALIDADORES ADMIN

def valida_formato_cpf(cpf):
    if re.search(r'[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}', cpf) == None:
        raise ValidationError('Formato do CPF inválido. Utilize o padrão xxx.xxx.xxx-xx')

def valida_cpf(raw_cpf):
    cpf = [int(char) for char in raw_cpf if char.isdigit()]

    if len(cpf) != 11:
        raise ValidationError('CPF Inválido')

    if cpf == cpf[::-1]:
        raise ValidationError('CPF Inválido')

    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            raise ValidationError('CPF Inválido')

def valida_cep(cep):
    if re.search(r'[0-9]{5}-[0-9]{3}', cep) == None:
        raise ValidationError('Formato do CEP inválido. Utilize o padrão xxxxx-xx')