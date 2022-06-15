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
