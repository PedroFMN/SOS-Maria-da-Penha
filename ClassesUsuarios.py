#CLASSES DOS USUÁRIOS DO SISTEMA: USUÁRIA E AGENTE

#CLASSE ABSTRATA CONTA
#SUBCLASSES: USUÁRIA E AGENTE

from enum import Enum

import json

class Conta:
    def __init__(self, nome, cpf, senha, telefone):
        self.nome = nome
        self.cpf = cpf
        self.senha = senha
        self.telefone = telefone
        self.gps = 0.0

        self.contatos = []
        self.notificacoes = []

    def mandar_mensagem(self, receptor):
        texto = input("Digite: ")

        self.criar_mensagem(receptor, texto)

    def criar_mensagem(self, receptor, texto):
        print("Mensagem enviada para: ", receptor)

        mensagem = {
            "remetente": self.nome,
            "texto": texto
        }
        receptor.receber_mensagem(mensagem)

    def receber_mensagem(self, mensagem):
        #CRIA UMA NOTIFICAÇÃO PARA O USUÁRIO RECEPTOR DA MENSAGEM
        nova_notificacao = {
            "tipo": "mensagem",
            "remetente": mensagem["remetente"],
            "titulo": "Nova mensagem recebida",
            "texto": mensagem["texto"],
        }

        self.adicionar_notificacao(nova_notificacao)
        print("Mensagem recebida de: ", nova_notificacao["texto"])

    def adicionar_notificacao(self, notificacao):
        if notificacao["tipo"] not in ["mensagem", "alerta", "aviso"]:
            print("Tipo de notificação inválido. Use 'mensagem', 'alerta' ou 'aviso'.")
            return

        self.notificacoes.append(notificacao)

        with open("usuarios_db.json", "r+") as dados:
            usuarios = json.load(dados)
            usuarios[self.cpf]["notificacoes"] = self.notificacoes
        with open("usuarios_db.json", "w", encoding="utf-8") as dados:
            json.dump(usuarios, dados, indent=4, ensure_ascii=False)

    def deletar_notificacao(self, indice):
        if 0 <= indice < len(self.notificacoes):
            del self.notificacoes[indice]

    def ler_notificacao(self, indice):
        if 0 <= indice < len(self.notificacoes):
            notificacao = self.notificacoes[indice]
            if notificacao["tipo"] == "mensagem":
                print(f"Mensagem de {notificacao['remetente']}: {notificacao['texto']}")
            return

        print("Indice inválido. Nenhuma notificação lida.")

    def ver_notificacoes(self):
        if not self.notificacoes:
            print("Nenhuma notificação.")
            return

        for i, notificacao in enumerate(self.notificacoes, start=1):
            print(f"{i}. {notificacao['titulo']}(Remetente: {notificacao.get('remetente', 'Sistema')})")

        if input("Deseja ler alguma notificação? (s/n): ").lower() == 's':
            indice = int(input("Digite o número da notificação que deseja ler: ")) - 1

            self.ler_notificacao(indice)
            self.deletar_notificacao(indice)

        return

    def ver_perfil(self):
        print("Nome:", self.nome)
        print("CPF:", self.cpf)
        print("Telefone:", self.telefone)

    def adicionar_contato(self, contato):
        self.contatos.append(contato)

    def ver_contatos(self):
        if not self.contatos:
            print("Nenhum contato disponível.")
            return

        print("Contatos:")
        for i, contato in enumerate(self.contatos, start=1):
            print(f"{i}. {contato.nome}")

        if input("Deseja enviar uma mensagem para algum contato? (s/n): ").lower() == 's':
            indice = int(input("Digite o número do contato que deseja enviar a mensagem: ")) - 1

            if 0 <= indice < len(self.contatos):
                receptor = self.contatos[indice]
                self.mandar_mensagem(receptor)
            else:
                print("Contato inválido.")
            return

    def adicionar_contato(self, contato):
        self.contatos.append(contato)

    def menu_principal(self, acoes):
        print("--- Menu da Conta ---")
        print("1. Ver perfil")
        print("2. Ver notificações")
        print("3. Ver contatos")
        print("4. Sair")

        escolha = input("Escolha uma opção: ")

        while True:
            if escolha == "1":
                return acoes.VER_PERFIL

            elif escolha == "2":
                return acoes.VER_NOTIFICACOES

            elif escolha == "3":
                return acoes.VER_CONTATOS

            elif escolha == "4":
                print("Saindo...")
                return acoes.OFF

            else:
                print("Opção inválida. Tente novamente.")

    def interface_usuario(self):
        class acoes(Enum):
            VER_PERFIL = 1
            VER_NOTIFICACOES = 2
            VER_CONTATOS = 3
            MENU = 4
            OFF = 6

        acao_do_momento = acoes.MENU

        while not acao_do_momento == acoes.OFF:
            if acao_do_momento == acoes.MENU:
                acao_do_momento = self.menu_principal(acoes)

            else:
                if acao_do_momento == acoes.VER_PERFIL:
                    self.ver_perfil()

                if acao_do_momento == acoes.VER_NOTIFICACOES:
                    self.ver_notificacoes()

                if acao_do_momento == acoes.VER_CONTATOS:
                    self.ver_contatos()

                acao_do_momento = acoes.MENU

class Usuaria(Conta):
    def __init__(self, nome, cpf, senha, telefone):
        super().__init__(nome, cpf, senha, telefone)
        self.guardioes = [] # Os guardiões são pessoas de confiança da usuária.
        self.medida_protetiva = "" # Medida protetiva da usuária, caso ela possua uma. Inicialmente, é uma string vazia.

    def cadastrar_guardiao(self, guardiao):
        self.guardioes.append(guardiao)
        with open("guardioes_db.json", "r") as dados :
            json.dump(guardiao)
        print(f"Guardião cadastrado: PLACEHOLDER") #TROCAR QUANDO FAZEREM A CLASSE.

    def ver_guardioes(self):    
        if not self.guardioes:
            print("Nenhum guardião cadastrado.")
        else:
            for guardiao in self.guardioes:
                print(f"Guardião: {guardiao.nome} - Telefone: {guardiao.telefone}")

        if len(self.guardioes) < 2:
            if input("Deseja cadastrar algum guardião? (s/n): ").lower() == 's':
                nome = input("Digite o nome do guardião: ")
                telefone = input("Digite o telefone do guardião: ")
                guardiao = "TESTE" 
                self.cadastrar_guardiao(guardiao)

    def cadastrar_medida_protetiva(self, medida):
        self.medida_protetiva = medida.nome_judicial
        print(f"Medida protetiva cadastrada: {self.medida_protetiva.nome_judicial}")

    def acionar_emergencia(self):
        print("Acionando emergência...")

        # PARA FAZER ESSA FUNÇÃO, PRIMEIRO PRECISAREMOS DE OUTROS SISTEMAS.

    def menu_principal(self, acoes):
        print("--- Menu da Conta ---")
        print("1. Ver perfil")
        print("2. Ver notificações")
        print("3. Ver contatos")
        print("4. Acionar Emergência")
        print("5. Ver guardiões")
        print("6. Sair")

        escolha = input("Escolha uma opção: ")

        while True:
            if escolha == "1":
                return acoes.VER_PERFIL

            elif escolha == "2":
                return acoes.VER_NOTIFICACOES

            elif escolha == "3":
                return acoes.VER_CONTATOS

            elif escolha == "4":
                return acoes.ACIONAR_EMERGENCIA

            elif escolha == "5":
                return acoes.VER_GUARDIOES

            elif escolha == "6":
                print("Saindo...")
                return acoes.OFF

            else:
                print("Opção inválida. Tente novamente.")

    def interface_usuario(self):
        class acoes(Enum):
            VER_PERFIL = 1
            VER_NOTIFICACOES = 2
            VER_CONTATOS = 3
            VER_GUARDIOES = 7
            MENU = 4
            ACIONAR_EMERGENCIA = 5
            OFF = 6

        acao_do_momento = acoes.MENU

        while not acao_do_momento == acoes.OFF:
            if acao_do_momento == acoes.MENU:
                acao_do_momento = self.menu_principal(acoes)

            else:
                if acao_do_momento == acoes.VER_PERFIL:
                    self.ver_perfil()

                if acao_do_momento == acoes.VER_NOTIFICACOES:
                    self.ver_notificacoes()

                if acao_do_momento == acoes.VER_CONTATOS:
                    self.ver_contatos()

                if acao_do_momento == acoes.ACIONAR_EMERGENCIA:
                    self.acionar_emergencia()

                if acao_do_momento == acoes.VER_GUARDIOES:
                    self.ver_guardioes()

                acao_do_momento = acoes.MENU