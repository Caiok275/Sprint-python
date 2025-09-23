import os
import json

# Exames, doutores e horas disponíveis
exame_geral = {
    "Dr.José" : ["6:00", "10:00", "14:00"],
    "Dra.Maria" : ["8:00", "12:00", "16:00"]}

exame_de_sangue = {
    "Dr.Pedro" : ["8:00", "12:00", "16:00"],
    "Dr.Ana" :  ["9:00", "13:00", "17:00"]}

raioX = {
    "Dr.Lucas": ["7:30", "11:30", "15:30"]}

ultraSom = {
    "Dr.João" : ["6:00", "10:00", "14:00"],}

doutores = [exame_geral, exame_de_sangue, raioX, ultraSom]
tipos_consulta = ["Exame Geral", "Exame de Sangue", "Raio X", "Ultrassom"]

arq_doutores = "doutores.json"

# ================= Funções =================

# Apaga o terminal independente do sistema operacional
def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# Lê o arquivo "usuario.txt" e retorna um dicionario "usuario"
def ler_usuario(arq_usuario: str) -> dict:
    usuario = {}
    try:
        with open(arq_usuario, "r", encoding="utf-8") as f:
            for linha in f:
                email, senha = linha.strip().split(":")
                usuario[email] = senha
    except FileNotFoundError:
        pass  # Se não houver arquivo, apenas retorna vazio
    return usuario

# Recebe o endereço de email e senha e implementa no dicionario "usuario"
def criar_usuario(arq_usuario: str ,usuario: dict) -> None:
    while True:
        limpar_tela()
        email = solicitar_email(usuario) 
        if email is None:
            return  # Usuário optou por voltar
        senha = solicitar_senha()
        confirmar = confirmar_dados(email, senha)
        if confirmar == False:
            continue # Usuário decidiu refazer seu cadastro
        usuario[email] = senha
        input("\nUsuário cadastrado com sucesso! Pressione ENTER para continuar...\n")
        gravar_usuario(arq_usuario,usuario)
        break

# Pergunta ao usuário seu email, e o retorna vazio caso digite 0
def solicitar_email(usuario: dict) -> str | None:
    while True:
        email = input("Digite seu Email ou pressione 0 para voltar: ")
        if email == "0":
            return
        elif email in usuario:
            limpar_tela()
            print("\nEste endereço de email já está cadastrado. Tente novamente.\n")
        elif email == "":
            limpar_tela()
            print("É um endereço de Email para se cadastrar\n")
        else:
            return email
        
# Pergunta o usuário uma senha e recusa senha "vazia"
def solicitar_senha() -> str:
    while True:
        senha = input("Digite uma senha:")
        if senha == "":
            limpar_tela()
            print("É necessario digitar uma senha para se dastrar\n")
            continue
        else:
            return senha

# Pergunta se todos os dados inseridos estão de acordo
def confirmar_dados(email: str, senha: str) -> bool:
    print("\nConfira os dados antes de registrar:")
    print(f"Email: {email}")
    print(f"Senha: {senha}\n")

    while True:
        confirmacao = input("Os dados estão corretos? (sim/não): ").strip().lower()
        if confirmacao in ("sim", "s"):
            return True
        elif confirmacao in ("não", "nao", "n"):
            input("\nOK, pressione ENTER para tentar novamente...\n")
            return False
        else:
            print("Resposta inválida. Digite 'sim' ou 'não'.")

# Grava email e senha em um arquivo .txt
def gravar_usuario(arq_usuario: str, usuario: dict) -> None:
    with open(arq_usuario, "w", encoding="utf-8") as f:
        for email, senha in usuario.items():
            f.write(f"{email}:{senha}\n")

# Verifica se o email e senha condizem
def autentificacao(usuario: dict) -> bool:
    while True:
        print("Digite seu Email e Senha ou digite 0 para cancelar:\n")
        email = input("Email:")
        if email == "0":
            break
        senha = input("Senha:")
        if senha == "0":
            break
        liberado = conferir_credencial(usuario, email, senha)
        if liberado == False:
            limpar_tela()
            print("Senha ou Email incorreto!!!")
            continue
        else:
            limpar_tela()
            input("Login realizado com sucesso, pressione ENTER para continuar...")
            return True

# Confere se a senha e o email está correto
def conferir_credencial(usuario: dict, email: str, senha: str) -> bool:
    return usuario.get(email) == senha

# ================= Tela de Login =================
def login():
    # TODO ver se dá pra converter para .json
    arq_usuario = "usuario.txt"
    usuario = ler_usuario(arq_usuario)
    while True:
        limpar_tela()
        print("-"*10, "Bem Vindo", "-"*10)
        print()
        print("1.Fazer Login")
        print("2.Não possui cadastro ainda? Digite 2 para Criar um usuário!")
        print()
        print("0.SAIR")

        # Estrutar match/case
        opcao = input("Digite uma das opções:")
        match opcao:
            case "0":
                limpar_tela()
                print("Finalizando o código...")
                break
            case "1": 
                limpar_tela()
                liberar = autentificacao(usuario)
                if liberar == True:
                    return True
            case "2":
                criar_usuario(arq_usuario,usuario)
            case _:
                limpar_tela()
                input("Selecione uma opção valida! Pressione ENTER para continuar...")

# ======== Funções do menu principal ========

# Grava todos os dados em um arquivo json
def gravar_doutores(arq_doutores: str, doutores: list):
    with open(arq_doutores, "w", encoding="utf-8") as f:
        json.dump(doutores, f, indent=4)

# Lê o documento doutores.json e retorna os dados
def ler_doutores(arq_doutores: str):
    try:
        with open(arq_doutores, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        pass  # Se não houver arquivo, apenas retorna vazio
    return dados

# Mostra todos os nomes dos doutores, seus tipos de consulta e status com base no número de horas disponíveis
def mostrar_todos_doutores(doutores: list, tipos_consulta: list) -> None:
    limpar_tela()
    print("-"*10, "Doutores", "-"*10)
    print()
    for i, tipo in enumerate(doutores):
        for nomes, h_disponiveis in tipo.items():
            if not h_disponiveis:
                status = "Indiponível"
            else:
                status = "Disponível"
            print(f"{nomes} - {tipos_consulta[i]} ({status})")
    input("Pressione ENTER para voltar ao menu principal...")

def marcar_consulta(doutores: list, tipos_consulta: list):
    mostrar_tipos_consulta(tipos_consulta)
    consulta_escolhida = escolher_consulta(doutores, tipos_consulta)
    disponiveis = doutores_disponiveis(consulta_escolhida)
    mostrar_doutores_disponiveis(disponiveis)
    doutor_escolhido = escolher_doutor(disponiveis)
    
    mostrar_h_disponiveis(disponiveis[doutor_escolhido])


def mostrar_tipos_consulta(tipos_consulta: list):
    limpar_tela()
    print("-"*10, "Consultas", "-"*10)
    print()
    for i, tipo in enumerate(tipos_consulta, start=1):
        print(i, tipo)

def escolher_consulta(doutores: list, tipos_consultas: list):
    while True:
        try:
            escolha = int(input("Escolha uma das consultas:"))
            if escolha == 0:
                limpar_tela()
                input("Pressione ENTER para voltar ao menu principal...")
                break
            elif escolha < 0 or escolha > len(tipos_consulta):
                limpar_tela()
                input("Opção invalida, pressione ENTER para tentar novamente...")   
            else:
                return doutores[escolha-1]
        except ValueError:
            limpar_tela()
            input("Opção invalida, pressione ENTER para tentar novamente...")          

def doutores_disponiveis(doutores:list):
    disponiveis = {}
    for nome, horas in exame_geral.items():
        if horas:
            disponiveis[nome] = horas
    return disponiveis

def mostrar_doutores_disponiveis(disponiveis: dict):    
    limpar_tela()
    print("-"*10, "Doutores Disponíveis", "-"*10)
    print()
    for i, nome in enumerate(disponiveis, start=1):
        print(f"{i}.{nome}")

def escolher_doutor(disponiveis: dict):
    for i, nome in enumerate(disponiveis, start=1):
        try:
            escolha = int(input("\nEscolha um(a) doutor(a) ou pressione 0 para voltar:"))
            if escolha == 0:
                limpar_tela()
                input("Pressione ENTER para voltar ao menu principal...")
                break
            elif escolha < 1 or escolha > i:
                print("Escolha inválida...")            
            else:
                return i -1
        except ValueError:
            input("Opção invalida, pressione ENTER para tentar novamente...")   

def mostrar_h_disponiveis(disponiveis: dict):
    limpar_tela()
    print("-"*10, "Horas Disponíveis", "-"*10)
    print()
    for nome, h_disponivel in doutores.items():
        print(f"{nome} - ", ",".join(h_disponivel))

# ================= Menu Principal =================
def menu():
    limpar_tela()
    
    arq_agenda = "agenda.txt"

    agenda = {}

    doutores = ler_doutores(arq_doutores)
    while True:
        print("-"*10, "Menu Principal", "-"*10)
        print()
        print("1.Marcar consulta")
        print("2.Ver status da consulta")
        print("3.Cancelar consulta")
        print("4.Ver todos os Doutores")
        print()
        print("0.SAIR")

        opcao = input("Digite uma das opções:")
        match opcao:
            case "0":
                limpar_tela()
                print("Finalizando o código...")
                break
            case "1":
                marcar_consulta(doutores, tipos_consulta)
            case "4":
                mostrar_todos_doutores(doutores, tipos_consulta)
            case _:
                limpar_tela()
                input("Selecione uma opção valida! Pressione ENTER para continuar...")

# ================= Execução =================
login = login()
if login == True:

    menu()

