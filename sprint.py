import os

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


# ======== Funções do menu principal ========
 
# Mostra o nome de todos os doutores, sua especialidade e seus status
def mostrar_doutor(doutores: dict) -> None:
    limpar_tela()
    print("-"*10, "Doutores", "-"*10, "\n")
    for nome, informacao in doutores.items():
        tipo_consulta = informacao["Tipo de exame"]
        if informacao["Disponivel"]:
            status = "Disponivel"
        else:
            status = "Indisponivel"
        print(f"{nome} - {tipo_consulta} ({status})")
    input("\nPressione ENTER para votar ao menu...")

def marcar_consulta(doutores: dict, agenda: dict) -> None:
    while True:
        limpar_tela()
        print("-"*10, "Marcar Exame", "-"*10)
        print()
        print("Escolha o tipo de Exame:")
        print("1.Raio-X")
        print("2.Exame de sangue")
        print("3.Exame geral")
        print("4.Ultrassom")
        print()
        print("0.Voltar")

        opcao = input("Digite uma das opções:")
        match opcao:
            case "0":
                limpar_tela()
                input("Voltando para o menu principal, Pressione ENTER para continuar...")
                break
            case "1":
                limpar_tela()
                tipo = "Raio-X"
                buscar_doutor(doutores, tipo)
            case "2":
                limpar_tela()
                tipo = "Exame de sangue"
                buscar_doutor(doutores, tipo)
            case "3":
                limpar_tela()
                tipo = "Exame geral"
                buscar_doutor(doutores, tipo)
            case "4":
                limpar_tela()
                tipo = "Ultrassom"
                buscar_doutor(doutores, tipo)
            case _:
                limpar_tela()
                input("Selecione uma opção valida! Pressione ENTER para continuar...")

# Função que pega o tipo de consulta selecionada e mostra na tela junto com os nomes dos doutores que fazer o tipo de exame selecionado
# TODO filtrar todos os doutores com a key "Disponivel" como False
def buscar_doutor(doutores:dict, tipo: str) -> None:
    limpar_tela()
    print(f"-"*10, tipo, "-"*10, "\n")
    for nome, informacoes in doutores.items():
        if tipo in informacoes["Tipo de exame"]:
            h_disponivel = informacoes["Horas disponíveis"]
            print(f"{nome} - Horas disponíveis: {h_disponivel}")
    input("\nPressione ENTER para voltar ao menu principal...")



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


            

    
# ================= Menu Principal =================
def menu():
    limpar_tela()
    
    arq_agenda = "agenda.txt"

    agenda = {}
    doutores = {
        "Dr.Jose": {
            "Tipo de exame" : "Exame geral",
            "Horas disponíveis" : ["6:00", "10:00", "14:00"],
            "Numero da sala" : "101",
            "Disponivel" : True
        },
        "Dra.Maria": {
            "Tipo de exame": "Exame de sangue",
            "Horas disponíveis": ["8:00", "12:00", "16:00"],
            "Numero da sala": "102",
            "Disponivel": True
        },
        "Dr.Pedro": {
            "Tipo de exame": "Exame de sangue",
            "Horas disponíveis": ["7:30", "11:30", "15:30"],
            "Numero da sala": "103",
            "Disponivel": True
        },
        "Dra.Ana": {
            "Tipo de exame": "Raio-X",
            "Horas disponíveis": ["9:00", "13:00", "17:00"],
            "Numero da sala": "104",
            "Disponivel": False
        },
        "Dr.Lucas": {
            "Tipo de exame": "Exame geral",
            "Horas disponíveis": ["6:30", "10:30", "14:30"],
            "Numero da sala": "105",
            "Disponivel": True
        },
        "Dr.João": {
            "Tipo de exame": "Ultrassom",
            "Horas disponíveis": ["6:00", "10:00", "14:00"],
            "Numero da sala": "201",
            "Disponivel": True
        }

    }

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
                marcar_consulta(doutores, agenda)
            case "4":
                mostrar_doutor(doutores)
            case _:
                limpar_tela()
                input("Selecione uma opção valida! Pressione ENTER para continuar...")

# ================= Execução =================
login = login()
if login == True:
    menu()