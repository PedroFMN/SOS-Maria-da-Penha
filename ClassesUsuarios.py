#CLASSES DOS USUÁRIOS DO SISTEMA: USUÁRIA E AGENTE

#CLASSE ABSTRATA
#SUBCLASSES: USUÁRIA E AGENTE

class Conta:
    def __init__(self, nome, cpf, senha, telefone):
        self.nome = nome
        self.cpf = cpf
        self.senha = senha
        self.telefone = telefone
        self.gps = 0.0
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
        

CONTA001 = Conta("Maria", "123.456.789-00", "senha123", "(11) 98765-4321")

CONTA001.adicionar_notificacao({
    "tipo": "mensagem",
    "remetente": "João",
    "titulo": "Nova mensagem",
    "texto": "Olá, como você está?"
})

CONTA001.ver_notificacoes()
CONTA001.ver_notificacoes()
