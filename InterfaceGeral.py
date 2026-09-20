# Código para os usuários usarem o sistema e  criar a database dos arquivos.

import json
from re import match

def interface_inicial():
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
            exit()

def criar_conta():
    if 