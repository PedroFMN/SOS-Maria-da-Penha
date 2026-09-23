import json

#NOTIFICAÇÕES DOS USUÁRIOS, EXISTEM SEMPRE DENTRO DO USUÁRIO
class Notificacao:
    def __init__(self,tipo,remetente,titulo,texto,data):
        self.tipo = tipo
        self.remetente = remetente
        self.titulo = titulo
        self.texto = texto
        self.data = data

#MENSAGENS ENVIADAS POR USUÁRIOS, EXISTEM SEMPRE DENTRO DO USUÁRIO
class Mensagem:
    def __init__(self,receptor,texto,data):
        self.receptor = receptor
        self.texto = texto
        self.data = data

# ARMAZENA OS DADOS DA EMERGENCIA QUE SERÃO ENVIADOS AO AGENTE E GUARDIÃO.
class Emergencia:
    def __init__(self,hora,local,vitima):
        self.hora = hora
        self.local = local
        self.vitima = vitima

    def getDate(self):
        return self.getDate

    def getLocal(self):
        return self.getLocal

    


    

    
     