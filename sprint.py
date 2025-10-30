import os

import json
import oracledb
import pandas as pd
from datetime import datetime

# Váriavel que armazena o nome do usuário após um login bem sucedido
usuario_logado = ""
# Exames, doutores e horas disponíveis

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

# Recebe o nome do usuário e senha e o implementa no dicionario "usuario"
def criar_usuario(arq_usuario: str ,usuario: dict) -> None:
    while True:
        limpar_tela()
        nome = solicitar_usuario(usuario) 
        if nome is None:
            return  # Usuário optou por voltar
        senha = solicitar_senha()
        if senha is None:
            return # Usuário optou por voltar
        pedir_confirmacao(nome, senha)
        confirmar = confirmar_dados()
        if confirmar == False:
            continue # Usuário decidiu refazer seu cadastro
        usuario[nome] = senha
        input("\nUsuário cadastrado com sucesso! Pressione ENTER para continuar...\n")
        dicionario_para_txt(arq_usuario,usuario)
        break

# Pergunta ao usuário seu nome e checa se o nome colocado já foi cadastrado antes
def solicitar_usuario(usuario: dict) -> str | None:
    while True:
        nome = input("Digite seu nome ou pressione 0 para voltar: ").strip().upper()
        if nome == "0":
            return
        elif nome in usuario:
            limpar_tela()
            print("\nEste nome já está cadastrado. Tente novamente.\n")
        elif nome == "":
            limpar_tela()
            print("É obrigatorio escrever o seu nome")
        else:
            return nome
        
# Pergunta o usuário uma senha e recusa senha "vazia"
def solicitar_senha() -> str:
    while True:
        senha = input("Digite uma senha:").strip()
        if senha == "0":
            return
        elif senha == "":
            limpar_tela()
            print("É necessario digitar uma senha para se dastrar\n")
            continue
        else:
            return senha

# Pergunta se todos os dados inseridos estão de acordo
def pedir_confirmacao(nome: str, senha:str):
    print("\nConfira os dados antes de registrar:")
    print(f"Nome: {nome}")
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

# Verifica se o nome e senha condizem
def autentificacao(usuario: dict) -> bool:
    while True:
        print("Digite seu nome e sua senha ou digite 0 para cancelar:\n")
        nome = input("Nome:").upper()
        if nome == "0":
            break # Usuário optou por voltar
        senha = input("Senha:")
        if senha == "0":
            break # Usuário optou por voltar
        liberado = conferir_credencial(usuario, nome, senha)
        if liberado == False:
            limpar_tela()
            print("Senha ou nome incorreto!!!")
            continue # nome ou senha incorretos
        else:
            # Atribui o nome autentificado na variável global usuario_logado e retorna o valor "True"
            global usuario_logado
            usuario_logado = nome
            limpar_tela()
            input("Login realizado com sucesso, pressione ENTER para continuar...")
            return True

# Confere se a senha e o email está correto
def conferir_credencial(usuario: dict, nome: str, senha: str) -> bool:
    for nome_correto, senha_correta in usuario.items():
        if nome == nome_correto and senha == senha_correta:
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
def agendar():
    while True:
        try:
            limpar_tela()
            print("----- Agendar Consulta -----")
            # Recebe os valores para cadastro
            global usuario_logado
            nm_paciente = usuario_logado

            escolha = selecionar_tipos_consulta()

            sql = """SELECT * FROM T_HCFMUSP_DOUTORES WHERE tipo_consulta = :1"""
            
            df = listar_doutores(sql,escolha)

            limpar_tela()
            print(df)
            id_doutor = int(input("Escolha um dos doutores "))

            data_str = input("Digite a data e a hora da consulta (DD/MM/YYYY) ").strip()

            dt_consulta = datetime.strptime(data_str, "%d/%m/%Y")
            sql = """ INSERT INTO T_HCFMUSP_CONSULTAS (nm_paciente,id_doutor,dt_consulta)VALUES (:1,:2,:3)"""
            inst_cadastro.execute(sql,(nm_paciente,id_doutor,dt_consulta))
            conn.commit()

        except ValueError:
            print("Digite um valor válido!")
        except:
            print("Erro na transação do BD")
        else:
            # Caso haja sucesso na gravação
            print("##### Dados GRAVADOS #####")

def selecionar_tipos_consulta():
    tipos_consulta = ["Exame Geral", "Exame de sangue", "Raio-X", "UltraSom"]
    print("Selecione o tipo de consulta:")
    for i, consulta in enumerate(tipos_consulta, start=1):
        print(f"{i}. {consulta}")
    try:
        escolha = int(input("\nDigite o número da consulta desejada: "))
        if escolha < 1 or escolha > len(tipos_consulta):
            print("Opção inválida.")
        else: 
            return tipos_consulta[escolha - 1]
        
    except ValueError:
        print("Digite um número")

def mostrar_todos_doutores(): 
    limpar_tela()
    sql = "SELECT * FROM T_HCFMUSP_DOUTORES"
    df = listar_doutores(sql)
    print("------ Doutores ------")
    print(df)

# funcao que lista todos os itens da tabela
def listar_doutores(sql: str, parametro: str = None) -> str:  
    lista_doutores = []  # Lista para captura de dados do Banco
    try:
        # Instrução SQL com base no que foi selecinado na tela de menu
        if not parametro:
            inst_consulta.execute(sql)
        else:
            inst_consulta.execute(sql,(parametro,))

        # Captura todos os registros da tabela e armazena no objeto data
        data = inst_consulta.fetchall()

        # Insere os valores da tabela na Lista
        for dt in data:
            lista_doutores.append(dt)

        # ordena a lista
        lista_doutores = sorted(lista_doutores)

        # Gera um DataFrame com os dados da lista utilizando o Pandas
        dados_df = pd.DataFrame.from_records(
            lista_doutores, columns=['id_doutor', 'nm_doutor', 'tipo_consulta'], index='id_doutor')
        
        # Verifica se não há registro através do dataframe
        if dados_df.empty:
            return "Nenhum doutor foi cadastrado"
        else:
            return dados_df
        
    except:
        print("Erro na transação do BD")

def mostrar_consultas() -> None:
    global usuario_logado
    sql = f"SELECT * FROM T_HCFMUSP_CONSULTAS WHERE nm_paciente = :1"
    parametro = usuario_logado
    df = listar_consultas(sql,parametro)
    if df.Empty:    
        print("Nenhuma consulta para remarcar")
    print(df)

# funcao que lista todos os itens da tabela
def listar_consultas(sql: str, parametro: str) -> str:  
    lista_consulta = []  # Lista para captura de dados do Banco
    try:
        global usuario_logado

        inst_consulta.execute(sql,(parametro,))

        # Captura todos os registros da tabela e armazena no objeto data
        data = inst_consulta.fetchall()

        # Insere os valores da tabela na Lista
        for dt in data:
            lista_consulta.append(dt)

        # ordena a lista
        lista_consulta = sorted(lista_consulta)

        # Gera um DataFrame com os dados da lista utilizando o Pandas
        dados_df = pd.DataFrame.from_records(
            lista_consulta, columns=['id_consulta', 'nm_paciente', 'id_doutor', 'dt_consulta'], index='id_consulta')
        
        # Verifica se não há registro através do dataframe
        if dados_df.empty:
            return "Nenhuma consulta foi registrada ainda"
        else:
            return dados_df
    except ValueError:
        print("Digite um valor válido!")
    except:
        print("Erro na transação do BD")

def remarcar_consulta():
    while True:
        try:
            limpar_tela()
            print("----- Remarcar Consulta -----")
            mostrar_consultas()
            id_consulta = input("Digite a consulta que deseja remarcar:")
            data_str = input("Digite a nova data e hora da consulta (DD/MM/YYYY) ").strip()
            dt_consulta = datetime.strptime(data_str, "%d/%m/%Y")
            sql = """ UPDATE T_HCFMUSP_CONSULTAS SET dt_consulta = :1 WHERE id_consulta = :2 """
            inst_alteracao.execute(sql, (dt_consulta,id_consulta))
            conn.commit()
        except ValueError:
            print("Digite um valor válido!")
        except:
            print("Erro na transação do BD")
        else:
            # Caso haja sucesso na gravação
            print("##### CONSULTA REMARCADA #####")

def cancelar_consulta():
    limpar_tela()
    try:
        print("----- Cancelar Consulta -----")
        mostrar_consultas()
        id_consulta = input("Digite a consulta que deseja cancelar:")
        confirmacao = input(f"Tem certeza que quer apagar a consulta {id_consulta}? (Sim/Não)").strip().lower()
        if confirmacao == "sim" or confirmacao == "s":
            sql = f""" DELETE FROM T_HCFMUSP_CONSULTAS WHERE id_consulta = :1 """
            # Executa a instrução e atualiza a tabela
            inst_exclusao.execute(sql, (id_consulta,))
            conn.commit()
            # Exibe mensagem caso haja sucesso
            print("##### CONSULTA CANCELADA! #####")
        else: 
            print("Deleção cancelada!")
    except:
        print("Erro na transação do BD")

def gerar_arquivo():
    nm_arquivo = input("Digite um nome para o arquivo (não digite a extenção):").strip()


# ================= Menu Principal =================
def menu():
    while True:
        limpar_tela()
        print("-"*10, "Menu Principal", "-"*10)
        print()
        print("1.Marcar consulta")
        print("2.Ver suas consultas")
        print("3. Remarcar consulta")
        print("4.Ver todos os Doutores")
        print("5.Gravar consulta em um arquivo json")
        print("6.CANCELAR Consulta")
        print()
        print("0.SAIR")

        opcao = input("Digite uma das opções:")

        match opcao:
            case "0":
                sair()
                break
            case "1":
                agendar()
            case "2":
                mostrar_consultas()
            case "3":
                remarcar_consulta()
            case "4":
                mostrar_todos_doutores()
            case "5":
                gerar_arquivo()
            case "6":
                cancelar_consulta()
            case _:
                limpar_tela()
                print("Selecione uma opção valida!")
        input("Pressione ENTER para continuar...")

def sair():
    global conexao
    limpar_tela()
    print("Obrigado por utilizar o nosso código")
    conexao = False

# ================= Conexão =================
try :
    conn = oracledb.connect(user = "rm562979",password = "251004",dsn = "oracle.fiap.com.br:1521/ORCL")
    inst_cadastro = conn.cursor()
    inst_consulta = conn.cursor()
    inst_alteracao = conn.cursor()
    inst_exclusao= conn.cursor()

except Exception as e:
    print(e)
    conexao=False
else:
    conexao=True

while conexao:
    login = login()
    if login == True:
        menu()

