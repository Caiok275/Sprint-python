import os

# Váriavel que armazena o email do usuário após um login bem sucedido
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

# Lê um arquivo .txt e retorna um dicionário
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
        if senha is None:
            return # Usuário optou por voltar
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
        if senha == "0":
            return
        elif senha == "":
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

# Pergunta se todos os dados estão corretos e retorna um valor boolean dependendo da resposta
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

# Grava um dicionário em um arquivo .txt
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
            break # Usuário optou por voltar
        senha = input("Senha:")
        if senha == "0":
            break # Usuário optou por voltar
        liberado = conferir_credencial(usuario, email, senha)
        if liberado == False:
            limpar_tela()
            print("Senha ou Email incorreto!!!")
            continue # Email e senha incorretos
        else:
            # Atribui o Email autentificado na variável global email_logado e retorna o valor "True"
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

    arq_usuario = "usuario.txt"
    while True:
        # lê o arquivo usuario.txt e retorna em um dicionário usuario
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
# Mostra todos os tipos de consulta
def mostrar_tipos_consulta(tipos_exame: list) -> None:
    limpar_tela()
    print("-"*10, "Tipos de consulta","-"*10)
    print()
    for i, tipos in enumerate(tipos_exame, start=1):
        print(f"{i}.{tipos}")
    print()

    return selecionar_consulta(tipos_exame)

# Pergunta o tipo de consulta e retorna a opção para ser usado como index da lista doutores
def selecionar_consulta(tipos_exame: list) -> int:
    while True:
        try:
            opcao = int(input("Selecione uma das consultas:"))
            if opcao < 1 or opcao > len(tipos_exame):
                print("Esta opção não existe, tente novamente")
            else:
                return opcao -1
        except (TypeError,ValueError):
            input("Esta opção não existe, pressione ENTER para tentar novamente...")

# Mostra apenas os doutores que realiza o tipo de consulta selecionada
def mostrar_doutores(doutores: dict) -> str:
    limpar_tela()
    print("-"*10, "Doutores", "-"*10)
    print()
    for nome, horas in doutores.items():
        print(f"{nome} - Horas disponíveis:", ", ".join(horas))
    
    return escolher(doutores, "Doutores")

# Mostra as horas disponíveis
def mostrar_horas(doutores: dict, dr_selecionado: dict):
    limpar_tela()
    horas = doutores[dr_selecionado]
    print("-"*10, "Horas Disponíveis", "-"*10)
    print()
    print(", ".join(horas))
    print()

    return escolher(horas, "Horas")

# Pergunta ao usuário qual doutor ou hora (dependendo da aplicação) e retorna a opção digitada
def escolher(dicionario: dict, nome_dicionario: str):
    if nome_dicionario == "Doutores":
        msg = "Escreva o nome de um dos doutores:"
    else:
        msg = "Escreva a hora da consulta:"
    while True:
        opcao = input(msg)
        if opcao == "0":
            limpar_tela()
            print("Voltando ao menu principal")
            return None
        elif opcao not in dicionario:

            print(f"{nome_dicionario} inválida, escreva exatamente como foi mostrado na tela")
        else:
            return opcao
        
# Pergunta ao usuário o tipo, o doutor e a hora da consulta e os junta em um dicionário consulta, caso todas as informações estejam satisfatórias, a consulta é gravada em um arquivo .txt
def marcar_consulta():
    while True:
        index_consulta = mostrar_tipos_consulta(tipos_exame)
        dr_selecionado = mostrar_doutores(doutores[index_consulta])
        horas_selecionadas = mostrar_horas(doutores[index_consulta], dr_selecionado)
        if not horas_selecionadas:
            break
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
            break
        else:
            continue

# Mostra o dicionário consulta de forma organizada
def exibir_consultas(consulta: dict) -> None:
    limpar_tela()
    print("-"*10,"consulta","-"*10)
    for key, value in consulta.items():
        print(f"{key}: {value}")
    print("-" * 30)

# Pergunta ao usuário um nome para dar ao arquivo .txt e o grava caso não exista arquivo com este nome previamente
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
            continue # Já exste arquivo com este nome

# Pergunta qual arquivo .txt o usuário gostaria de ver e caso o arquivo não pertença ao usuário, o arquivo o impede o arquivo de ser mostrado
def ver_consulta():
        nm_arq = input("\nEscreva o nome do arquivo a sua consulta foi salva (não escreva a extenção do arquivo):")
        nm_arq = nm_arq + ".txt"
        consulta = ler_arquivo(nm_arq)
        if not consulta:
            print("\nNão existe arquivo com este nome")
        elif email_logado != consulta["Usuário"]:
            print("A consulta gravada não pertence a esta conta, tente novamente.")
        else:
            exibir_consultas(consulta)
        
# Mostra todos os nomes dos doutores, seus tipos de consulta
def mostrar_todos_doutores(doutores: list, tipos_exame: list) -> None:
    limpar_tela()
    print("-"*20, "Doutores", "-"*20)
    print()
    for i, tipo in enumerate(doutores):
        for nomes, hora in tipo.items():
            print(f"{nomes} - {tipos_exame[i]}")
# ================= Menu Principal =================
def menu():
    while True:
        limpar_tela()
        print("-"*10, "Menu Principal", "-"*10)
        print()
        print("1.Marcar consulta")
        print("2.Ver suas consultas")
        print("3.Ver todos os Doutores")
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
            case "3":
                mostrar_todos_doutores(doutores, tipos_exame)
            case _:
                limpar_tela()
                print("Selecione uma opção valida!")
        input("Pressione ENTER para continuar...")

# ================= Execução =================
login = login()
if login == True:

    menu()

