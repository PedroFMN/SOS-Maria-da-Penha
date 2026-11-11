# Código para os usuários usarem o sistema e  criar a database dos arquivos.
# Se for testar o aplicativo, faça aqui.

# MEMBROS DO TRABALHO:
# Pedro Fernandes Martins Neto
# Julian Silva Medeiros
# Amanda Letícia Coelho de Souza
# João Marcos de Oliveira
# Luis Fabiano Rodrigues Star Domingos

# 2B DE INFORMÁTICA ANO DE 2026

import json

#BIBLIOTECAS DAS CLASSES:
import ClassesUsuarios
import ClassesLegais
import ClassesAplicativo

USUARIO_LOGADO = None #USUÁRIO QUE IRÁ USAR O SISTEMA AQUI!
LOGADO = False #VARIÁVEL PARA SABER SE O USUÁRIO ESTÁ LOGADO OU NÃO

# O CÓDIGO ESTÁ COMPLETO. A MAIORIA DAS COISAS ESTÃO FUNCIONANDO

#SE VOCÊ FOR TESTAR O CÓDIGO, TESTE AQUI! ISSO É A INTERFACE DE TODO USUÁRIO

def interface_inicial():
    while True:
        if not LOGADO:
            print("SOS MARIA DA PENHA - Sistema de Denúncia")
            print("1. Criar conta")
            print("2. Entrar na conta")
            print("Qualquer outra digitação sairá do aplicativo.")

            try:
                opcao = int(input())
            except ValueError:
                print("Entrada inválida. Digite apenas números.")
                continue

            match opcao:
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
    try:
        with open("usuarios_db.json", "r") as arquivo:
            usuarios = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        usuarios = {}

    nome = str(input("Digite seu nome: "))

    while True:
        class ExceçãoLimiteDigitos(Exception):
            pass
        cpf = str(input("Digite seu CPF (apenas números): "))
        if len(cpf) == 11 and cpf.isdigit() and cpf not in usuarios:
            break
        ExceçãoLimiteDigitos("CPF inválido. Digite um CPF válido com 11 dígitos.")

    while True:
        senha = str(input("Digite sua senha (mínimo 6 caracteres): "))
        if len(senha) >= 6:
            break
        ExceçãoLimiteDigitos("Senha inválida. A senha deve ter no mínimo 6 caracteres.")

    while True:
        telefone = str(input("Digite seu telefone (apenas números): "))
        if len(telefone) == 8 and telefone.isdigit() and telefone not in usuarios:
            break
        ExceçãoLimiteDigitos("Telefone inválido. Digite um telefone válido com pelo menos 8 dígitos ou que já não está cadastrado.")

    nova_conta = {
        "nome": nome,
        "cpf": cpf,
        "senha": senha,
        "telefone": telefone,
        "guardioes": [],
        "notificacoes": [],
        "contatos": [],
        "medida_protetiva": ""
    }


    adicionar_dado_usuario(nova_conta, cpf, usuarios)


def adicionar_dado_usuario(conta, cpf, usuarios):
    usuarios[cpf] = conta

    try:
        with open("usuarios_db.json", "w") as arquivo:
            json.dump(usuarios, arquivo, indent=4)
    except IOError:
        print("Erro ao salvar os dados no arquivo.")

def login():
    try:
        with open("usuarios_db.json", "r") as arquivo:
            usuarios = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Banco de dados de usuários não encontrado ou corrompido.")
        return

    cpf = str(input("Digite seu CPF: "))
    senha = str(input("Digite sua senha: "))

    if cpf in usuarios and usuarios[cpf]["senha"] == senha:
        global USUARIO_LOGADO, LOGADO
        usuario_dados = usuarios[cpf]

        guardioes = []

        for guardiao in usuario_dados["guardioes"]:
            try:
                with open("guardioes_db.json", "r") as guardioes_arquivo:
                    guardioes_data = json.load(guardioes_arquivo)
                    guardiao_info = guardioes_data[guardiao]
                    if guardiao_info:
                        guardioes.append(ClassesLegais.Guadiao(guardiao_info["nome"], guardiao_info["protegendo"], guardiao_info["telefone"], guardiao_info["email"]))
            except (FileNotFoundError, KeyError, json.JSONDecodeError):
                continue
        
        contato = []

        #
        for contato_item in usuario_dados["contatos"]:
            try:
                contato.append(contato_item["nome"])
            except (TypeError, KeyError):
                continue

        notificacao_obj = []

        for notificacao in usuario_dados["notificacoes"]:
            try:
                notificacao_obj.append(ClassesAplicativo.Notificacao(notificacao["tipo"], notificacao["remetente"], notificacao["titulo"], notificacao["texto"], notificacao["data"]))
            except (KeyError, TypeError):
                continue
        

        medida_protetiva = ""
        if usuario_dados["medida_protetiva"]:
            try:
                mp = usuario_dados["medida_protetiva"]
                ag = mp["agressor"]
                tor = mp["tornozeleira"]
                medida_protetiva = ClassesLegais.MedidaProtetiva(mp["nome_judicial"], mp["distancia"], mp["distancia"], mp["data_inicio"], mp["validacao"], ClassesLegais.Agressor(ag["nome"], ag["cpf"], ag["telefone"]), mp["agressor_com_tornozeleira"], ClassesLegais.Tornozeleira(tor["modelo"], tor["usuario"], tor["distancia"], tor["data_de_checagem"]))
            except (KeyError, TypeError):
                medida_protetiva = ""

        USUARIO_LOGADO = ClassesUsuarios.Usuaria(usuario_dados["nome"], usuario_dados["cpf"], usuario_dados["senha"], usuario_dados["telefone"], guardioes, medida_protetiva, notificacao_obj, contato)

        LOGADO = True
        print(f"Bem-vindo(a), {USUARIO_LOGADO.nome}!")
        # Aqui você pode chamar a função para acessar o menu principal do sistema
    else:
        print("CPF ou senha incorretos. Tente novamente.")



interface_inicial()