import os
import json

email_logado = ""
# Exames, doutores e horas disponíveis
exame_geral = {
    "Dr.Ricardo" : ["6:00", "10:00", "14:00"],
    "Dra.Maria" : ["8:00", "12:00", "16:00"]}

exame_de_sangue = {
    "Dr.Pedro" : ["8:00", "12:00", "16:00"],
    "Dr.Ana" :  ["9:00", "13:00", "17:00"]}

raioX = {
    "Dr.Lucas": ["7:30", "11:30", "15:30"]}

ultrassom = {
    "Dr.Vitor" : ["6:00", "10:00", "14:00"],}

doutores = [exame_geral, exame_de_sangue, raioX, ultrassom]
tipos_exame = ["Exame geral", "Exame de sangue", "Raio-X", "Ultrassom"]

arq_doutores = "doutores.json"

# ================= Funções gerais =================

# ================= Funções Tela de Login =================

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
        # Pergunta se ele quer refazer o cadastr
        mostrar_confirmar_dados(email,senha)
        confirmar = confirmar_dados()
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
def mostrar_confirmar_dados(email:str, senha: str):
    print("\nConfira os dados antes de registrar:")
    print(f"Email: {email}")
    print(f"Senha: {senha}\n")

def confirmar_dados() -> bool:
    while True:
        confirmacao = input("Os dados estão corretos? (sim/não): ").strip().lower()
        if confirmacao in ("sim", "s"):
            return True
        elif confirmacao in ("não", "nao", "n"):
            input("OK, pressione ENTER para tentar novamente...")
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
            global email_logado
            email_logado = email
            limpar_tela()
            input("Login realizado com sucesso, pressione ENTER para continuar...")
            return True

# Confere se a senha e o email está correto
def conferir_credencial(usuario: dict, email: str, senha: str) -> bool:
    for email_correto,senha_correta in usuario.items():
        if email == email_correto and senha == senha_correta:
            return True
        else:
            return False

# ================= Tela de Login =================
def login():
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

def selecionar_consulta():
    while True:
        limpar_tela()
        print("-"*10, "Tipos de consulta","-"*10)
        print()
        for i, tipo in enumerate(tipos_exame, start=1):
            print(f"{i}.{tipo}")
        print()
        try:
            opcao = int(input("Selecione uma das consultas:"))
            if opcao >= 1 or opcao <= len(tipos_exame):
                return opcao -1
        except TypeError:
            limpar_tela()
            input("Não existe a opção selecionada, pressione ENTER para tentar novamente...")
                
def doutor_disponivel(consulta_selecionada):
    dr_disponiveis = {}
    for nome, horas in consulta_selecionada.items():
        if horas:
            dr_disponiveis[nome] = horas
    return dr_disponiveis

def escolher_doutor(dr_disponiveis):
    while True:
        limpar_tela()
        print("-"*10, "Doutores", "-"*10)
        print()
        if not dr_disponiveis:
            print("Infelizmente todos os doutores estão ocupados ")
            input("pressione ENTER para voltar ao menu principal")
            break
        else:
            for nome, horas in dr_disponiveis.items():
                print(f"{nome} - Horas disponíveis:", ", ".join(horas))
            opcao = input("\nEscreva o nome de um dos doutores (Escreva apenas o nome do doutor):")
            if opcao not in dr_disponiveis:
                print("Doutor não encontrado, digite o nome exatamente como foi mostrado\n")
            elif opcao == "0":
                limpar_tela()
                input("pressione ENTER para voltar ao menu principal")
                break
        return opcao
        
def escolher_horas(dr_disponiveis,dr_selecionado):
    while True:
        limpar_tela()
        horas = dr_disponiveis[dr_selecionado]
        print("-"*10, "Horas Disponíveis", "-"*10)
        print()
        print(", ".join(horas))
        print()

        opcao = input("Escreva a hora da consulta:")

        if opcao not in horas:
            limpar_tela()
            print("Hora inválida (lembre-se de colocar : entre hora e minuto)")
            input("Digite ENTER para continuar")
        elif opcao == "0":
            limpar_tela()
            input("pressione ENTER para voltar ao menu principal")
            break
        else:
            return opcao
        
# Mostra todos os nomes dos doutores, seus tipos de consulta e status com base no número de horas disponíveis
def mostrar_todos_doutores(doutores: list) -> None:
    limpar_tela()
    print("-"*10, "Doutores", "-"*10)
    print()
    for i, tipo in enumerate(doutores):
        for nomes, h_disponiveis in tipo.items():
            if not h_disponiveis:
                status = "Indiponível"
            else:
                status = "Disponível"
            print(f"{i}.{nomes} ({status})")
    input("Pressione ENTER para voltar ao menu principal...")

def marcar_consulta(arq_agenda: str):
    index_consulta = selecionar_consulta()
    dr_disponiveis = doutor_disponivel(doutores[index_consulta])
    dr_selecionado = escolher_doutor(dr_disponiveis)
    horas_selecionadas = escolher_horas(dr_disponiveis, dr_selecionado)
    consulta = {
        "Email" : email_logado,
        "Tipo" : tipos_exame[index_consulta],
        "Doutor" : dr_selecionado,
        "Hora" : horas_selecionadas
        }
    mostrar_consulta(consulta)
    confirmar = confirmar_dados()
    if not confirmar:
        return
    else:
        doutores[index_consulta][dr_selecionado].remove(horas_selecionadas)
        input(doutores[index_consulta])
    limpar_tela()
    print("Consulta realizada com sucesso")
    gravar_dicionario_json(consulta,arq_agenda)
    input("\nPressione ENTER para voltar ao menu inícial.")

def gravar_dicionario_json(info: dict,arq_json: str):
    with open(arq_json, "a", encoding="utf-8") as f:
        json.dump(info, f, indent=4)
    print("Consulta salva na agenda")

def ler_json(arq_json: str):
    arquivo = {}
    try:
        with open(arq_json, "r", encoding="utf-8") as f:
            arquivo = json.load(f)
    except FileNotFoundError:
        pass  # Se não houver arquivo, apenas retorna vazio
    return arquivo
    
def mostrar_consulta(consulta: dict) ->None:
    limpar_tela()
    print("-"*10, "Consulta" ,"-"*10)
    if not consulta:
        input("Nenhuma consulta foi agendada ainda, pressione ENTER para voltar")
        pass
    for v, k in consulta.items():
        print(f"{v} - {k}")
# ================= Menu Principal =================
def menu():
    
    arq_agenda = "agenda.json"
    agenda = ler_json(arq_agenda)

    while True:
        limpar_tela()
        print("-"*10, "Menu Principal", "-"*10)
        print()
        print("1.Marcar consulta")
        print("2.Ver suas consultas")
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
                marcar_consulta(arq_agenda)
            case "2":
                mostrar_consulta(agenda)
                input("\nPressione ENTER para continuar...")
            case "4":
                mostrar_todos_doutores(doutores)
            case _:
                limpar_tela()
                print("Selecione uma opção valida!")

# ================= Execução =================
login = login()
if login == True:

    menu()

