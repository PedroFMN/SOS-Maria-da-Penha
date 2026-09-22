class Medida_Protetiva:
    def __init__(self, nomejudicial, distancia, data_inicio, validacao):
        self.nomejudicial = nomejudicial
        self.distancia = distancia
        self.data = data_inicio
        self.validacao = validacao

    def getAgressor(self, Agressor):
        return Agressor
    
    def getDistancia(self):
        self.GPS_vitima - self.GPS_agressor == self.distancia
        return self.distancia
    
    def getNomejudicial(self, nomejudicial):
        return nomejudicial
    
    def getVitima(self, Vitima):
        return Vitima
    
    def atualizarDados(self, novo_nomejudicial, novo_distancia, novo_data_inicio, novo_validacao):
        self.nomejudicial = novo_nomejudicial
        self.distancia = novo_distancia
        self.data = novo_data_inicio
        self.validacao = novo_validacao

class Guadiao:
    def __init__(self, nome, protegendo, numero, email):
        self.nome = nome
        self.protegendo = protegendo
        self.telefone = numero
        self.email = email

    def receberEmergencia(self, gps_proteger):
        usuario = Guadiao
        mensagem = print("Mensagem de Emergência - Localização: ", gps_proteger)

        if self.telefone :
           print(mensagem)
        elif usuario == self.email:
           print(mensagem)
        elif usuario == self.telefone and usuario == self.email:
           print(mensagem)
        
        
    def receberSMS(self, gps_protegendo):
        print("Mensagem de Emergência - Localização: ", gps_protegendo)
        

    def receberEmail(self, gps_protegendo):
        print("Mensagem de Emergência - Localização: ", gps_protegendo)