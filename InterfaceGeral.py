# Código para os usuários usarem o sistema e  criar a database dos arquivos.

import json

USUARIO_ATUAL = None #USUÁRIO QUE IRÁ USAR O SISTEMA AQUI!

def interface_inicial():
    print("SOS MARIA DA PENHA - Sistema de Denúncia")
    print("1. Criar conta")
    print("2. Entrar na conta")
    print("Qualquer outra digitação sairá do aplicativo.")
    match int(input()):
        case 1:
            criar_conta()
        case 2:
            #login()
            pass
        case _:
            print("Saindo do aplicativo...")
            exit()

def criar_conta():
    with open("usuarios_db.json", "r") as arquivo:
        usuarios = json.load(arquivo)

    nome = str(input("Digite seu nome: "))

    while True:
        cpf = str(input("Digite seu CPF (apenas números): "))
        if len(cpf) == 11 and cpf.isdigit() and cpf not in usuarios:
            break
        print("CPF inválido. Digite um CPF válido com 11 dígitos.")

    while True:
        senha = str(input("Digite sua senha (mínimo 6 caracteres): "))
        if len(senha) >= 6:
            break
        print("Senha inválida. A senha deve ter no mínimo 6 caracteres.")

    while True:
        telefone = str(input("Digite seu telefone (apenas números): "))
        if len(telefone) == 8 and telefone.isdigit() and telefone not in usuarios:
            break
        print("Telefone inválido. Digite um telefone válido com pelo menos 8 dígitos.")

    nova_conta = {
        "nome": nome,
        "cpf": cpf,
        "senha": senha,
        "telefone": telefone,
        "guardioes": [],
        "notificacoes": [],
        "medida_protetiva": "",
    }


    adicionar_dado_usuario(nova_conta, cpf, usuarios)


def adicionar_dado_usuario(conta, cpf, usuarios):

    usuarios[cpf] = conta

    with open("usuarios_db.json", "w") as arquivo:
        json.dump(usuarios, arquivo, indent=5)

criar_conta()