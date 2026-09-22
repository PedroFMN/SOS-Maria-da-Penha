# Código para os usuários usarem o sistema e  criar a database dos arquivos.

import json

#BIBLIOTECAS DAS CLASSES:
import ClassesUsuarios

USUARIO_LOGADO = None #USUÁRIO QUE IRÁ USAR O SISTEMA AQUI!
LOGADO = False #VARIÁVEL PARA SABER SE O USUÁRIO ESTÁ LOGADO OU NÃO

def interface_inicial():
    while True:
        if not LOGADO:
            print("SOS MARIA DA PENHA - Sistema de Denúncia")
            print("1. Criar conta")
            print("2. Entrar na conta")
            print("Qualquer outra digitação sairá do aplicativo.")

            match int(input()):
                case 1:
                    criar_conta()
                case 2:
                    login()
                case _:
                    print("Saindo do aplicativo...")
                    exit("Aplicativo fechado!.")
        else:
            USUARIO_LOGADO.interface_usuario()

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
        print("Telefone inválido. Digite um telefone válido com pelo menos 8 dígitos ou que já não está cadastrado.")

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
        json.dump(usuarios, arquivo, indent=4)

def login():
    with open("usuarios_db.json", "r") as arquivo:
        usuarios = json.load(arquivo)

    cpf = str(input("Digite seu CPF: "))
    senha = str(input("Digite sua senha: "))

    if cpf in usuarios and usuarios[cpf]["senha"] == senha:
        global USUARIO_LOGADO, LOGADO
        usuario_dados = usuarios[cpf]
        USUARIO_LOGADO = ClassesUsuarios.Usuaria(usuario_dados["nome"], usuario_dados["cpf"], usuario_dados["senha"], usuario_dados["telefone"], usuario_dados["guardioes"], usuario_dados["medida_protetiva"], usuario_dados["notificacoes"])
        LOGADO = True
        print(f"Bem-vindo(a), {USUARIO_LOGADO.nome}!")
        # Aqui você pode chamar a função para acessar o menu principal do sistema
    else:
        print("CPF ou senha incorretos. Tente novamente.")

interface_inicial()