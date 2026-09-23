class Notificacao:
    def __init__(self,tipo,remetente,titulo,texto,data):
        self.tipo = tipo
        self.remetente = remetente
        self.titulo = titulo
        self.texto = texto
        self.data = data
    


class Mensagem:
    def __init__(self,receptor,texto,data):
        self.receptor = receptor
        self.texto = texto
        self.data = data


class Emergencia:
    def __init__(self,hora,local):
        self.hora = hora
        self.local = local

    def getDate(self):
        return self.getDate

    def getLocal(self):
        return self.getLocal

    


    

    
     