#CLASSES DOS USUÁRIOS DO SISTEMA: USUÁRIA E AGENTE

#CLASSE ABSTRATA CONTA
#SUBCLASSES: USUÁRIA E AGENTE

from enum import Enum

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
        notificacao = {
            "tipo": "mensagem",
            "remetente": mensagem["remetente"],
            "titulo": "Nova mensagem recebida",
            "texto": mensagem["texto"],
        }

        self.adicionar_notificacao(notificacao)
        print("Mensagem recebida de: ", notificacao["texto"])

    def adicionar_notificacao(self, notificacao):
        if notificacao["tipo"] not in ["mensagem", "alerta", "aviso"]:
            print("Tipo de notificação inválido. Use 'mensagem', 'alerta' ou 'aviso'.")
            return

        self.notificacoes.append(notificacao)

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
            print(f"{i}. {contato}")

        if input("Deseja enviar uma mensagem para algum contato? (s/n): ").lower() == 's':
            indice = int(input("Digite o número do contato que deseja enviar a mensagem: ")) - 1

            if 0 <= indice < len(self.contatos):
                receptor = self.contatos[indice]
                self.mandar_mensagem(receptor)
            else:
                print("Contato inválido.")
            return

    def menu_principal(self, acoes):
        print("--- Menu da Conta ---")
        print("1. Ver perfil")
        print("2. Ver notificações")
        print("3. Ver contatos")
        print("4. Enviar mensagem")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        while True:
            if escolha == "1":
                return acoes.VER_PERFIL

            elif escolha == "2":
                return acoes.VER_NOTIFICACOES

            elif escolha == "3":
                return acoes.VER_CONTATOS

            elif escolha == "4":
                return acoes.ENVIAR_MENSAGEM

            elif escolha == "5":
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
            ENVIAR_MENSAGEM = 5
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

                if acao_do_momento == acoes.ENVIAR_MENSAGEM:
                    self.ver_contatos()

                acao_do_momento = acoes.MENU

Boneco = Conta("Boneco", "123.456.789-00", "senha123", "99999-9999")

Boneco.interface_usuario()