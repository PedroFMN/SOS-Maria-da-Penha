#CLASSES DOS USUÁRIOS DO SISTEMA: USUÁRIA E AGENTE

#CLASSE ABSTRATA CONTA
#SUBCLASSES: USUÁRIA E AGENTE

from enum import Enum

import ClassesLegais
import ClassesAplicativo

import json

class Conta:
    def __init__(self, nome, cpf, senha, telefone, notificacoes, contatos):
        self.nome = nome
        self.cpf = cpf
        self.senha = senha
        self.telefone = telefone
        self.gps = 0.0

        self.contatos = contatos
        self.notificacoes = notificacoes

    def mandar_mensagem(self, receptor):
        texto = input("Digite: ")

        self.criar_mensagem(receptor, texto)

    def criar_mensagem(self, receptor, texto):
        print("Mensagem enviada para: ", receptor)

        mensagem = {
            "remetente": self.nome,
            "texto": texto
        }

        with open("agentes_db.json", "r+") as dados:
            usuarios = json.load(dados)
            #PROCURE O AGENTE NO JSON:
            for agente in usuarios.values():
                if agente["nome"] == receptor:
                    #CRIE UMA INSTANCIA DA CLASSE AGENTE AQUI!
                    receptor_da_mensagem = Agente(agente["nome"], agente["cpf"], agente["senha"], agente["telefone"], agente["central_de_seguranca"], agente["matricula"])
                    break
        receptor_da_mensagem.receber_mensagem(mensagem)

    def receber_mensagem(self, mensagem):
        #CRIA UMA NOTIFICAÇÃO PARA O USUÁRIO RECEPTOR DA MENSAGEM

        nova_notificacao = {
            "tipo": "mensagem",
            "remetente": mensagem["remetente"],
            "titulo": "Nova mensagem recebida",
            "texto": mensagem["texto"],
        }

        self.adicionar_notificacao(nova_notificacao)

    def adicionar_notificacao(self, notificacao):
        if notificacao["tipo"] not in ["mensagem", "alerta", "aviso"]:
            print("Tipo de notificação inválido. Use 'mensagem', 'alerta' ou 'aviso'.")
            return

        notificacao_classe = ClassesAplicativo.Notificacao(
            tipo=notificacao["tipo"],
            remetente=notificacao.get("remetente"),
            titulo=notificacao["titulo"],
            texto=notificacao["texto"],
            data=notificacao["data"]
        )

        self.notificacoes.append(notificacao_classe)

        with open("usuarios_db.json", "r+") as dados:
            usuarios = json.load(dados)
            usuarios[self.cpf]["notificacoes"] = self.notificacoes
        with open("usuarios_db.json", "w", encoding="utf-8") as dados:
            json.dump(usuarios, dados, indent=4, ensure_ascii=False)

    def deletar_notificacao(self, indice):
        if 0 <= indice < len(self.notificacoes):
            del self.notificacoes[indice]
        with open("usuarios_db.json", "r+") as dados:
            usuarios = json.load(dados)
            usuarios[self.cpf]["notificacoes"] = self.notificacoes
        with open("usuarios_db.json", "w", encoding="utf-8") as dados:
            json.dump(usuarios, dados, indent=4, ensure_ascii=False)

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

#SUBCLASSE DE Conta
#CLASSE PARA TODAS AS USUÁRIAS DO SISTEMA
#INTERAGEM COM A OUTRA SUBCLASSE DA CONTA, AGENTE, POR MEIO DE MENSAGENS E EMERGÊNCIAS.

class Usuaria(Conta):
    def __init__(self, nome, cpf, senha, telefone, guardioes, medida_protetiva, notificacoes, contatos):
        super().__init__(nome, cpf, senha, telefone, notificacoes, contatos)
        self.guardioes = guardioes # Os guardiões são pessoas de confiança da usuária.
        self.medida_protetiva = medida_protetiva # Medida protetiva da usuária, caso ela possua uma. Inicialmente, é uma string vazia.

    def cadastrar_guardiao(self, guardiao):
        #Relação de herança
        self.guardioes.append(guardiao)

        guardiao_dados ={
            "nome": guardiao.nome,
            "protegendo": guardiao.protegendo,
            "telefone": guardiao.telefone,
            "email": guardiao.email
        }

        with open("guardioes_db.json", "r") as dados :
            guardioes = json.load(dados)
            guardioes[guardiao.nome] = guardiao_dados

        with open("guardioes_db.json", "w") as dados :
            json.dump(guardioes, dados, indent=4)

        with open("usuarios_db.json", "r") as dados :
            usuarios = json.load(dados)
            usuarios[self.cpf]["guardioes"] = [guardiao.nome for guardiao in self.guardioes]
        
        with open("usuarios_db.json", "w") as dados :
            json.dump(usuarios, dados, indent=4)

        print(f"Guardião cadastrado!")

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
                guardiao_novo = ClassesLegais.Guadiao(nome, self.nome, telefone, "")
                self.cadastrar_guardiao(guardiao_novo)

    def acionar_emergencia(self):
        print("Acionando emergência...")
        with open("agentes_db.json", "r") as dados:
            agentes = json.load(dados)
            agentes_disponiveis = [agente for agente in agentes.values() if agente["ocorrencia_atual"] == None]
            if agentes_disponiveis:
                emergencia = ClassesAplicativo.Emergencia("00:00", self.gps, self.nome)
                agente = agentes_disponiveis[0]
                print(f"Agente {agente['nome']} acionado para a emergência.")
                agente["ocorrencia_atual"] = self.nome
                with open("agentes_db.json", "w") as dados:
                    json.dump(agentes, dados, indent=4)
                
            notificacao_obj = []
            for notificacao in agentes_disponiveis["notificacoes"]:
                notificacao_obj.append(ClassesAplicativo.Notificacao(notificacao["tipo"], notificacao["remetente"], notificacao["titulo"], notificacao["texto"], notificacao["data"]))

            agente_escolhido = Agente(agente["nome"], agente["cpf"], agente["senha"], agente["telefone"], agente["central_de_seguranca"], agente["matricula"], notificacao_obj)
            agente_escolhido.receber_ocorrencia(emergencia)
            for guardiao in self.guardioes:
                guardiao.receberEmergencia(self.gps)
            nao_esta = True
            for contato in self.contatos:
                if agente_escolhido.nome == contato.nome:
                    nao_esta = False
            if nao_esta:
                self.adicionar_contato(agente_escolhido)
                print(f"Agente {agente_escolhido.nome} adicionado aos contatos da usuária.")

    def menu_principal(self, acoes):
        print("--- Menu da Conta ---")
        print("1. Ver perfil")
        print("2. Ver notificações")
        print("3. Ver contatos")
        print("4. Acionar Emergência")
        print("5. Ver guardiões")
        print("6. Gerenciar medida protetiva")
        print("7. Sair")

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
                return acoes.GERENCIAR_MEDIDA_PROTETIVA

            elif escolha == "7":
                print("Saindo...")
                return acoes.OFF

            else:
                print("Opção inválida. Tente novamente.")

    def cadastrar_medida_protetiva(self, medida):
        self.medida_protetiva = medida.nomejudicial
        print(f"Medida protetiva cadastrada: {self.medida_protetiva}")

        tornozeleira_dados = {
            "modelo": medida.tornozeleira.modelo,
            "usuario": medida.tornozeleira.usuario,
            "distancia": medida.tornozeleira.distancia,
            "data_de_checagem": medida.tornozeleira.data_de_checagem,
        }

        medida_protetiva_dados = {
            "nome_judicial": medida.nomejudicial,
            "distancia": medida.distancia,
            "data_inicio": medida.data,
            "validacao": medida.validacao,
            "agressor": medida.agressor,
            "agressor_com_tornozeleira": medida.agressor_com_tornozeleira,
            "tornozeleira": tornozeleira_dados
        }

        with open("usuarios_db.json", "r") as dados:
            usuarios = json.load(dados)
            usuarios[self.cpf]["medida_protetiva"] = medida_protetiva_dados

        with open("usuarios_db.json", "w") as dados:
            json.dump(usuarios, dados, indent=4)


    def gerenciar_medida_protetiva(self):
        if self.medida_protetiva is not "":
            print(f"Medida protetiva atual: {self.medida_protetiva.nomejudicial}")

        else:
            if input("Deseja cadastrar uma medida protetiva? (s/n): ").lower() == 's':
                nome_judicial = input("Digite o nome judicial da medida protetiva: ")
                distancia = float(input("Digite a distância da medida protetiva (em metros): "))
                data_inicio = input("Digite a data de início da medida protetiva em ano: ")
                validacao = input("Digite a validação da medida protetiva: ")
                agressor = input("Digite o nome do agressor: ")
                agressor_com_tornozeleira = input("O agressor possui tornozeleira? (s/n): ").lower() == 's'

                medida = ClassesLegais.Medida_Protetiva(nome_judicial, distancia, data_inicio, validacao, agressor, agressor_com_tornozeleira)

                if agressor_com_tornozeleira:
                    modelo = input("Digite o modelo da tornozeleira: ")
                    tornozeleira = ClassesLegais.Tornozeleira(modelo, agressor, distancia, data_inicio)
                    medida.tornozeleira = tornozeleira
    
                self.cadastrar_medida_protetiva(medida)

    def interface_usuario(self):
        class acoes(Enum):
            VER_PERFIL = 1
            VER_NOTIFICACOES = 2
            VER_CONTATOS = 3
            VER_GUARDIOES = 7
            MENU = 4
            ACIONAR_EMERGENCIA = 5
            GERENCIAR_MEDIDA_PROTETIVA = 8
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

                if acao_do_momento == acoes.GERENCIAR_MEDIDA_PROTETIVA:
                    self.gerenciar_medida_protetiva()

                acao_do_momento = acoes.MENU
        exit()

#Relação de herança: SUBCLASSE DE CONTA
#INTERAGE COM A SUBCLASSE USUÁRIA POR MEIO DE MENSAGENS E EMERGÊNCIAS

class Agente(Conta):
    def __init__(self, nome, cpf, senha, telefone, notificacoes, contatos, central_de_seguranca, matricula, nivel_de_acesso="Agente"):
        super().__init__(nome, cpf, senha, telefone, notificacoes, contatos)
        self.central_de_seguranca = central_de_seguranca
        self.matricula = matricula
        self.nivel_de_acesso = nivel_de_acesso
        self.ocorrencia_atual = None
        self.historico_ocorrencias = []
        
        
        self.carregar_ou_salvar_json()

    def salvar_no_json(self):
      
        try:
            try:
                with open("usuarios_db.json", "r", encoding="utf-8") as dados:
                    usuarios = json.load(dados)
            except (FileNotFoundError, json.JSONDecodeError):
                usuarios = {}

            usuarios[self.cpf] = {
                "tipo_conta": "agente",
                "nome": self.nome,
                "cpf": self.cpf,
                "senha": self.senha,
                "telefone": self.telefone,
                "central_de_seguranca": self.central_de_seguranca,
                "matricula": self.matricula,
                "nivel_de_acesso": self.nivel_de_acesso,
                "notificacoes": self.notificacoes,
                "ocorrencia_atual": self.ocorrencia_atual,
                "historico_ocorrencias": self.historico_ocorrencias
            }

            with open("usuarios_db.json", "w", encoding="utf-8") as dados:
                json.dump(usuarios, dados, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[ERRO JSON] Falha ao salvar agente no JSON: {e}")

    def carregar_ou_salvar_json(self):
        
        try:
            with open("usuarios_db.json", "r", encoding="utf-8") as dados:
                usuarios = json.load(dados)
                if self.cpf in usuarios:
                    dados_agente = usuarios[self.cpf]
                    self.nome = dados_agente.get("nome", self.nome)
                    self.senha = dados_agente.get("senha", self.senha)
                    self.telefone = dados_agente.get("telefone", self.telefone)
                    self.central_de_seguranca = dados_agente.get("central_de_seguranca", self.central_de_seguranca)
                    self.matricula = dados_agente.get("matricula", self.matricula)
                    self.nivel_de_acesso = dados_agente.get("nivel_de_acesso", self.nivel_de_acesso)
                    self.notificacoes = dados_agente.get("notificacoes", self.notificacoes)
                    self.ocorrencia_atual = dados_agente.get("ocorrencia_atual", self.ocorrencia_atual)
                    self.historico_ocorrencias = dados_agente.get("historico_ocorrencias", self.historico_ocorrencias)
                    return
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        self.salvar_no_json()

    def ver_perfil(self):
        super().ver_perfil()
        print(f"Central de Segurança: {self.central_de_seguranca}")
        print(f"Matrícula: {self.matricula}")
        print(f"Nível de Acesso: {self.nivel_de_acesso}")
        if self.ocorrencia_atual:
            id_oc = self.ocorrencia_atual.get("id") if isinstance(self.ocorrencia_atual, dict) else getattr(self.ocorrencia_atual, "id", self.ocorrencia_atual)
            print(f"Ocorrência em Atendimento: ID {id_oc}")
        else:
            print("Status de Atendimento: Livre / Nenhuma ocorrência ativa")

    def editar_perfil(self):
        print("\n--- Editar Perfil do Agente ---")
        print("Deixe em branco e pressione Enter se não quiser alterar o campo.")
        
        novo_nome = input(f"Novo Nome [{self.nome}]: ")
        if novo_nome.strip():
            self.nome = novo_nome

        novo_telefone = input(f"Novo Telefone [{self.telefone}]: ")
        if novo_telefone.strip():
            self.telefone = novo_telefone

        nova_central = input(f"Nova Central de Segurança [{self.central_de_seguranca}]: ")
        if nova_central.strip():
            self.central_de_seguranca = nova_central

        nova_senha = input("Nova Senha: ")
        if nova_senha.strip():
            self.senha = nova_senha

        self.salvar_no_json()
        print("Perfil do agente atualizado e sincronizado com o banco de dados!")

    def receber_ocorrencia(self, ocorrencia=None):
        if ocorrencia is None:
            print("\n--- Receber Nova Ocorrência ---")
            id_oc = input("Digite o ID ou protocolo da ocorrência: ")
            vitima_nome = input("Digite o nome da vítima: ")
            local = input("Digite o local/endereço da ocorrência: ")
            ocorrencia = {
                "id": id_oc,
                "vitima": vitima_nome,
                "local": local,
                "status": "Em atendimento"
            }

        self.ocorrencia_atual = ocorrencia
        self.historico_ocorrencias.append(ocorrencia)
        self.salvar_no_json()

        vitima = ocorrencia.get("vitima") if isinstance(ocorrencia, dict) else getattr(ocorrencia, "vitima", "Não especificada")
        local = ocorrencia.get("local") if isinstance(ocorrencia, dict) else getattr(ocorrencia, "local", "Não especificado")

        print(f"\n[SUCESSO] Ocorrência atribuída ao agente {self.nome}!")
        print(f"-> Vítima: {vitima}")
        print(f"-> Local: {local}")

    def encerrar_ocorrencia(self):
        print("\n--- Encerrar Ocorrência ---")
        if not self.ocorrencia_atual:
            print("Nenhuma ocorrência ativa no momento para ser encerrada.")
            return

        id_oc = self.ocorrencia_atual.get("id") if isinstance(self.ocorrencia_atual, dict) else getattr(self.ocorrencia_atual, "id", "Atual")
        relatorio = input(f"Digite o relatório final para o encerramento da ocorrência {id_oc}: ")

        if isinstance(self.ocorrencia_atual, dict):
            self.ocorrencia_atual["status"] = "Encerrada"
            self.ocorrencia_atual["relatorio"] = relatorio

        print(f"[CONCLUÍDO] Ocorrência {id_oc} finalizada e arquivada no histórico.")
        self.ocorrencia_atual = None
        self.salvar_no_json()

    def gerenciar_medida_protetiva(self, cpf_usuaria, acao, nova_medida=""):
        
        try:
            with open("usuarios_db.json", "r", encoding="utf-8") as dados:
                usuarios = json.load(dados)

            if cpf_usuaria not in usuarios:
                print(f"[ERRO] Usuária com CPF {cpf_usuaria} não encontrada no banco de dados.")
                return

            if acao == "consultar":
                medida = usuarios[cpf_usuaria].get("medida_protetiva", "Nenhuma registrada.")
                print(f"\n--- Consulta de Medida Protetiva (CPF: {cpf_usuaria}) ---")
                print(f"Status/Descrição: {medida}")
            
            elif acao == "atualizar":
                usuarios[cpf_usuaria]["medida_protetiva"] = nova_medida
                with open("usuarios_db.json", "w", encoding="utf-8") as dados:
                    json.dump(usuarios, dados, indent=4, ensure_ascii=False)
                print(f"[SUCESSO] Medida protetiva da usuária CPF {cpf_usuaria} atualizada!")

        except Exception as e:
            print(f"[ERRO JSON] Não foi possível gerenciar medida protetiva: {e}")

    def gerenciar_conta(self, cpf_usuario, acao, novos_dados=None):
        
        try:
            with open("usuarios_db.json", "r", encoding="utf-8") as dados:
                usuarios = json.load(dados)

            if cpf_usuario not in usuarios:
                print(f"[ERRO] Usuário/Usuária com CPF {cpf_usuario} não encontrado(a).")
                return

            if acao == "bloquear":
                usuarios[cpf_usuario]["status_conta"] = "Bloqueada"
                print(f"[SUCESSO] Conta {cpf_usuario} bloqueada pelo agente {self.nome}.")
            elif acao == "desbloquear":
                usuarios[cpf_usuario]["status_conta"] = "Ativa"
                print(f"[SUCESSO] Conta {cpf_usuario} desbloqueada pelo agente {self.nome}.")
            elif acao == "atualizar" and novos_dados:
                usuarios[cpf_usuario].update(novos_dados)
                print(f"[SUCESSO] Dados da conta {cpf_usuario} atualizados pelo agente.")

            with open("usuarios_db.json", "w", encoding="utf-8") as dados:
                json.dump(usuarios, dados, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"[ERRO JSON] Falha no gerenciamento da conta: {e}")