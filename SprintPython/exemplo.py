'''
"6. Exibir Aprovados e Reprovados"
        Considere média mínima para aprovação de 6 pontos. 
        Mostre primeiro todos os Aprovados e depois os reprovados. Para todos, exiba as notas ao lado
"7. Gravar 'aprovados.txt' e 'aprovados.txt'"
        Gravar em um arquivo "aprovados.txt" os nomes e notas dos aprovados. 
        Gravar em um arquivo "reprovados.txt" os nomes e notas dos Reprovados
"8. Exibir os nomes dos alunos que tiraram a nota máxima"    
'''
# --------- FUNÇÕES AUXILIARES ---------
import os
# Grava o dicionário no arquivo formato: Nome:Nota
def gravar_notas(arquivo: str, notas: dict) -> None:
    with open(arquivo, "w") as f:
        for aluno, nota in notas.items():
            f.write(f"{aluno}:{nota}\n")

# Lê o arquivo texto e retorna um dicionário com as notas.
def ler_notas(arquivo: str) -> dict:
    notas = {}
    try:
        with open(arquivo, "r") as f:
            for linha in f:
                aluno, nota = linha.strip().split(":")
                notas[aluno] = float(nota)
    except FileNotFoundError:
        pass  # Se não houver arquivo, apenas retorna vazio
    return notas


# Cadastra um novo aluno e sua nota no dicionário.

def cadastrar_aluno(notas: dict) -> None:
    aluno = input("Nome do aluno: ")
    nota = float(input("Nota do aluno: "))
    notas[aluno] = nota
    print(f"Aluno {aluno} cadastrado com nota {nota}.")

# Calcula a média das notas de todos os alunos cadastrados.
def calcular_media(notas: dict) -> float:

    if len(notas) == 0:
        return 0.0
    return sum(notas.values()) / len(notas)

# Retorna o nome e a nota do aluno com maior nota.
def maior_nota(notas: dict) -> tuple:
    if len(notas) == 0:
        return ("", 0.0)
    aluno_top = max(notas, key=notas.get)
    return aluno_top, notas[aluno_top]

#    Exibe as notas cadastradas, uma por linha no formato: Nome - Nota
def exibir_notas(notas: dict) -> None:
    if len(notas) == 0:
        print("Nenhum aluno cadastrado.")
    else:
        print("\n--- NOTAS CADASTRADAS ---")
        for aluno, nota in notas.items():
            print(f"{aluno:10s} - {nota:4.1f}")


# --------- MENU PRINCIPAL ---------
def menu():
    arquivo = "notas.txt"
    notas = ler_notas(arquivo)  # Recupera dados salvos anteriormente

    while True:
        os.system("clear")
        print("\n--- MENU ---")
        print("1. Cadastrar novo aluno")
        print("2. Exibir todas as notas")
        print("3. Calcular média geral")
        print("4. Mostrar aluno com maior nota")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        # Estrutura match/case (Python 3.10+)
        match opcao:
            case "1":
                cadastrar_aluno(notas)
                gravar_notas(arquivo, notas)

            case "2":
                exibir_notas(notas)

            case "3":
                media = calcular_media(notas)
                print(f"Média geral das notas: {media:.2f}")

            case "4":
                aluno, nota = maior_nota(notas)
                print(f"Maior nota: {aluno} com {nota:.2f}")

            case "5":
                print("Encerrando programa.")
                break

            case _:
                print("Opção inválida, tente novamente.")

        input("\nPressione algo para continuar...")
# --------- EXECUÇÃO ---------
menu() 