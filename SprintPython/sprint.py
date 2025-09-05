import os

# ---------- Funções ----------

# Apaga o terminal independente do sistema operacional
def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# Lê o arquivo "usuario.txt" e retorna um dicionario "usuario"
def ler_usuario(arq_usuario: str) -> dict:
    usuario = {}
    try:
        with open(arq_usuario, "r") as f:
            for linha in f:
                email, senha = linha.strip().split(":")
                usuario[email] = senha
    except FileNotFoundError:
        pass  # Se não houver arquivo, apenas retorna vazio
    return usuario

def criar_usuario(usuario: dict) -> None: 
    limpar_tela()
    email = input("Digite seu Email:")
    senha = input("Digite uma senha:")
    usuario[email] = senha
    print(f"\nUsuário cadastrado com succeso! Confira os dados...") 
    print(f"Email:{email}") 
    print(f"Senha:{senha}\n")

def gravar_usuario(arq_usuario: str, usuario: dict) -> None:
    with open(arq_usuario, "w") as f:
        for email, senha in usuario.items():
            f.write(f"{email}:{senha}\n")

def conferir_credencial(usuario: dict, email: str, senha: str) -> bool:
    return usuario.get('email') == email and usuario.get('senha') == senha


# ---------- Tela de Login ----------
def login():
    arq_usuario = "usuario.txt"
    usuario = ler_usuario(arq_usuario)
    while True:
        limpar_tela()
        print("---------- Bem Vindo ----------\n" \
        "\n1:Para relaizar login digite 1" \
        "\n0:Não possui cadastro ainda? Digite 0 para Criar um usuário!\n")

        opcao = input("Digite uma das opções:")
        if opcao == "0":
            criar_usuario(usuario)
            gravar_usuario(arq_usuario,usuario)
        else:
            limpar_tela()
            print("Digite seu Email e Senha ou digite 0 para cancelar:\n")
            email = input("Email:")
            if email == "0":
                continue
            senha = input("Senha:")
            conferir_credencial(usuario, email, senha)
            
            

    
# ---------- Menu Principal ----------


def menu():
    arq_agenda = "agenda.txt"

    doutor = {
        1:José,
        2:Wilson,
        3:Giovana,
        4:Catarina,
        5:Pedro
    }

# ---------- Execução ----------
login()