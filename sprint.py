import os
import json

email_logado = ""
# Exames, doutores e horas disponíveis
exame_geral = {
    "Dr.Ricardo" : ["6h00", "10h00", "14h00"],
    "Dra.Maria" : ["8h00", "12h00", "16h00"]}

exame_de_sangue = {
    "Dr.Pedro" : ["8h00", "12h00", "16h00"],
    "Dr.Ana" :  ["9h00", "13h00", "17h00"]}

raioX = {
    "Dr.Lucas": ["7h30", "11h30", "15h30"]}

ultraSom = {
    "Dr.Vitor" : ["6h00", "10h00", "14h00"],}

doutores = [exame_geral, exame_de_sangue, raioX, ultraSom]
tipos_exame = ["Exame geral", "Exame de sangue", "Raio-X", "UltraSom"]

# ================= Funções =================

# Apaga o terminal independente do sistema operacional
def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# Lê o arquivo "usuario.txt" e retorna um dicionario "usuario"
def ler_arquivo(nm_arq: str) -> dict:
    dados = {}
    try:
        with open(nm_arq, "r", encoding="utf-8") as f:
            for linha in f:
                key, value = linha.strip().split(":")
                dados[key] = value
    except FileNotFoundError:
        pass  # Se não houver arquivo, apenas retorna vazio
    return dados

# Recebe o endereço de email e senha e implementa no dicionario "usuario"
def criar_usuario(arq_usuario: str ,usuario: dict) -> None:
    while True:
        limpar_tela()
        email = solicitar_email(usuario) 
        if email is None:
            return  # Usuário optou por voltar
        senha = solicitar_senha()
        pedir_confirmacao(email, senha)
        confirmar = confirmar_dados()
        if confirmar == False:
            continue # Usuário decidiu refazer seu cadastro
        usuario[email] = senha
        input("\nUsuário cadastrado com sucesso! Pressione ENTER para continuar...\n")
        dicionario_para_txt(arq_usuario,usuario)
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
def pedir_confirmacao(email: str, senha:str):
    print("\nConfira os dados antes de registrar:")
    print(f"Email: {email}")
    print(f"Senha: {senha}\n")

def confirmar_dados() -> bool:
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
def dicionario_para_txt(nm_arq: str, dicionario: dict) -> None:
    with open(nm_arq, "a", encoding="utf-8") as f:
        for key, value in dicionario.items():
            f.write(f"{key}:{value}\n")

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
    for email_correto, senha_correta in usuario.items():
        if email == email_correto and senha == senha_correta:
            return True
    return False

# ================= Tela de Login =================
def login():
    # TODO ver se dá pra converter para .json
    arq_usuario = "usuario.txt"
    while True:
        usuario = ler_arquivo(arq_usuario) 
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

def selecionar_consulta(tipos_exame: list):
    while True:
        limpar_tela()
        print("-"*10, "Tipos de consulta","-"*10)
        print()
        for i, tipos in enumerate(tipos_exame, start=1):
            print(f"{i}.{tipos}")
        print()

        try:
            opcao = int(input("Selecione uma das consultas:"))
            
            if opcao < 1 or opcao > len(tipos_exame):
                print("Esta opção não existe, tente novamente")
            else:
                return opcao -1
        except (TypeError,ValueError):
            input("Esta opção não existe, pressione ENTER para tentar novamente...")

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
                limpar_tela()
                input("Doutor não encontrado, digite o nome exatamente como foi mostrado. Pressione ENTER para continuar...")
            elif opcao == "0":
                limpar_tela()
                input("pressione ENTER para voltar ao menu principal")
                break
            else:
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
def mostrar_todos_doutores(doutores: list, tipos_exame: list) -> None:
    limpar_tela()
    print("-"*20, "Doutores", "-"*20)
    print()
    for i, tipo in enumerate(doutores):
        for nomes, h_disponiveis in tipo.items():
            if not h_disponiveis:
                status = "Indiponível"
            else:
                status = "Disponível"
            print(f"{nomes} - {tipos_exame[i]} ({status})")

def marcar_consulta():
    while True:
        index_consulta = selecionar_consulta(tipos_exame)
        dr_disponiveis = doutor_disponivel(doutores[index_consulta])
        dr_selecionado = escolher_doutor(dr_disponiveis)
        horas_selecionadas = escolher_horas(dr_disponiveis, dr_selecionado)
        consulta = {
            "Usuário" : email_logado,
            "Tipo de consulta" : tipos_exame[index_consulta],
            "Doutor" : dr_selecionado,
            "Hora" : horas_selecionadas
            }
        limpar_tela()
        exibir_consultas(consulta)
        confirmacao = confirmar_dados()
        if confirmacao:
            print("\nConsulta realizada com sucesso a consulta será gravada em um arquivo txt\n")
            gravar_consulta(consulta)
            doutores[index_consulta][dr_selecionado].remove(horas_selecionadas)
            break
        else:
            continue

# Exibe as consultas
def exibir_consultas(consulta):
    limpar_tela()
    print("-"*10,"consulta","-"*10)
    for key, value in consulta.items():
        print(f"{key}: {value}")
    print("-" * 30)

def gravar_consulta(dicionario: dict) -> None:
    while True:
        try:
            nm_arq = input("Digite um nome para o arquivo txt (não digite o nome com a extenção .txt):")
            with open(nm_arq + ".txt", "x", encoding="utf-8") as f:
                for key, value in dicionario.items():
                    f.write(f"{key}:{value}\n")
            print("Arquivo gravado com sucesso!")
            break
        except FileExistsError:
            print("Um arquivo com este nome já existe, tente novamente")
            continue
            
def ver_consulta():
        nm_arq = input("\nEscreva o nome do arquivo a sua consulta foi salva (não escreva a extenção do arquivo):")
        nm_arq = nm_arq + ".txt"
        consulta = ler_arquivo(nm_arq)
        print(consulta)
        print(consulta["Usuário"])
        if not consulta:
            print("\nNão existe arquivo com este nome")
        elif email_logado != consulta["Usuário"]:
            print("A consulta gravada não pertence a esta conta, tente novamente.")
        else:
            print(consulta)
            print(consulta["Usuário"])
            # exibir_consultas(consulta)
        


# ================= Menu Principal =================
def menu():

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
                marcar_consulta()
            case "2":
                ver_consulta()
            case "4":
                mostrar_todos_doutores(doutores, tipos_exame)
            case _:
                limpar_tela()
                input("Selecione uma opção valida!")
        input("Pressione ENTER para continuar...")

# ================= Execução =================
login = login()
if login == True:

    menu()

