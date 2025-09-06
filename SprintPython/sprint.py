import os

# ---------- Funções ----------

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
            print("Digite um endereço de Email")
        else:
            return email
        
# Pergunta o usuário uma senha e recusa senha "vazia"
def solicitar_senha() -> str:
    while True:
        senha = input("Digite uma senha:")
        if senha == "":
            limpar_tela()
            print("Digite uma senha:")
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

# ---------- Tela de Login ----------
def login():
    arq_usuario = "usuario.txt"
    usuario = ler_usuario(arq_usuario)
    while True:
        limpar_tela()
        print("------------- Bem Vindo -------------\n" \
        "\n1:Fazer login" \
        "\n2:Não possui cadastro ainda? Digite 2 para Criar um usuário!\n" \
        "\n0:SAIR")

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

            
            
            
            

    
# ---------- Menu Principal ----------


def menu():
    limpar_tela()
    
    arq_agenda = "agenda.txt"

    # doutor = {
    #     1:José,
    #     2:Wilson,
    #     3:Giovana,
    #     4:Catarina,
    #     5:Pedro
    # }

    print("---------- Menu Principal ----------")

# ---------- Execução ----------
login = login()
if login == True:
    menu()