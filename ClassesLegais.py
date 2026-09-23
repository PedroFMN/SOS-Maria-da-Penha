import json

#TODA MEDIDA PROTETIVA CADASTRADA
#É A CLASSE ONDE ARMAZENA A OUTRA CLASSE AGRESSOR, SEM A MEDIDA PROTETIVA, NÃO EXISTE AGRESSOR NO SISTEMA! (RELAÇÃO DE COMPOSIÇÃO)

class Medida_Protetiva:
    def __init__(self, nomejudicial, distancia, data_inicio, validacao, agressor, agressor_com_tornozeleira):
        self.nomejudicial = nomejudicial
        self.distancia = distancia
        self.data = data_inicio
        self.validacao = validacao
        self.agressor = agressor
        self.agressor_com_tornozeleira = agressor_com_tornozeleira
        self.tornozeleira = None

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

#ESSA É A CLASSE GUARDIÃO, NA QUAL É UMA PESSOA DE CONFIANÇA DA USUÁRIA, A CLASSE GUARDIÃO SEMPRE ESTÁ DENTRO DA CLASSE USUÁRIA (RELAÇÃO DE COMPOSIÇÃO)
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

#A TORNOZELEIRA É A TORNOZELEIRA USADA PELO AGRESSOR, AMBOS O AGRESSOR E A TORNOZELEIRA EXISTEM APENAS DENTRO DA CLASSE MEDIDA PROTETIVA (RELAÇÃO DE COMPOSIÇÃO)
#PORÉM NEM TODO AGRESSOR PODE POSSUIR UMA TORNOZELEIRA

class Tornozeleira:
    def __init__(self,modelo,usuario,distancia,data_de_checagem):
        self.identificacao = 0
        self.modelo = modelo
        self.usuario = usuario
        self.distancia = distancia
        self.data_de_checagem = data_de_checagem

  
    def get_modelo(self):
        return self.modelo

    def get_distancia(self):
        return self.distancia

    def get_usuario(self):
        return self.usuario

    def get_data(self):
        return self.data_de_checagem

    def prorrogar(self):
        return self.data_de_checagem

    def revogar(self):
        pass

# A CLASSE AGRESSOR IDENTIFICA O AGRESSOR DA MEDIDA PROTETIVA, A MEDIDA PROTETIVA PRECISA SEMPRE DE UM AGRESSOR. (COMPOSIÇÃO)
class Agressor:

    def _init_(self,nome,gps,cpf,vitima,medida_protetiva):
        # Atributos do Agressor
        self.nome = nome
        self.esta_com_tornozeleira = False
        self.gps = gps
        self.cpf = cpf
        self.vitima = vitima
        self.medida_protetiva = medida_protetiva

    
        self.tornozeleira = None

 
    def get_gps(self):
        return self.gps

    def get_medida_protetiva(self):
        return self.medida_protetiva

    def tem_tornozeleira(self):
        return self.esta_com_tornozeleira