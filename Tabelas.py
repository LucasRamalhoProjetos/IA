import os
import csv
from datetime import datetime

# Cria a pasta "Tabelas" se não existir
if not os.path.exists("Tabelas"):
    os.makedirs("Tabelas")

# Caminhos para os arquivos das tabelas (agora em CSV)
TABELA_FRASES = "Tabelas/frases.csv"
TABELA_SENSACOES = "Tabelas/sensacoes.csv"
TABELA_CONTEXTO = "Tabelas/contexto.csv"
TABELA_RESPOSTAS = "Tabelas/respostas.csv"
TABELA_APRENDIZADO = "Tabelas/aprendizado.csv"
TABELA_PALAVRAS = "Tabelas/palavras.csv"
TABELA_QUEMSOU = "Tabelas/quemsou.csv"
TABELA_ALFABETO = "Tabelas/alfabeto.csv"  # Nova tabela para o alfabeto

# Função para criar uma tabela CSV se não existir
def criar_tabela(caminho, cabecalho):
    if not os.path.exists(caminho):
        with open(caminho, "w", newline="", encoding="utf-8") as arquivo_csv:
            escritor_csv = csv.writer(arquivo_csv)
            escritor_csv.writerow(cabecalho)

# Cria as tabelas CSV com seus cabeçalhos
criar_tabela(TABELA_FRASES, ["id", "frase", "peso", "origem", "data_cadastro"])
criar_tabela(TABELA_SENSACOES, ["id", "emocao", "valor", "data_atualizacao"])
criar_tabela(TABELA_CONTEXTO, ["id", "id_frase", "resposta_sugerida", "data"])
criar_tabela(TABELA_RESPOSTAS, ["id", "id_frase", "resposta", "confianca"])
criar_tabela(TABELA_APRENDIZADO, ["id", "id_frase", "novo_peso", "confianca_nova", "data"])
criar_tabela(TABELA_PALAVRAS, ["palavra", "peso"])
criar_tabela(TABELA_QUEMSOU, ["id", "atributo", "valor", "peso", "origem", "data_cadastro"])
criar_tabela(TABELA_ALFABETO, ["letra", "tipo", "frequencia"])  # Cabeçalho para a tabela do alfabeto

# Função para adicionar uma nova frase à tabela de frases (CSV)
def adicionar_frase(frase, peso, origem):
    with open(TABELA_FRASES, "a", newline="", encoding="utf-8") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        id_novo = contar_linhas_csv(TABELA_FRASES) + 1
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        escritor_csv.writerow([id_novo, frase, peso, origem, data])
    return id_novo

# Função para adicionar uma nova sensação à tabela de sensações (CSV)
def adicionar_sensacao(emocao, valor):
    with open(TABELA_SENSACOES, "a", newline="", encoding="utf-8") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        id_novo = contar_linhas_csv(TABELA_SENSACOES) + 1
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        escritor_csv.writerow([id_novo, emocao, valor, data])

# Função para adicionar um novo contexto à tabela de contexto (CSV)
def adicionar_contexto(id_frase, resposta_sugerida):
    with open(TABELA_CONTEXTO, "a", newline="", encoding="utf-8") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        id_novo = contar_linhas_csv(TABELA_CONTEXTO) + 1
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        escritor_csv.writerow([id_novo, id_frase, resposta_sugerida, data])

# Função para adicionar uma nova resposta à tabela de respostas (CSV)
def adicionar_resposta(id_frase, resposta, confianca):
    with open(TABELA_RESPOSTAS, "a", newline="", encoding="utf-8") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        id_novo = contar_linhas_csv(TABELA_RESPOSTAS) + 1
        escritor_csv.writerow([id_novo, id_frase, resposta, confianca])

# Função para adicionar um novo registro de aprendizado (CSV)
def adicionar_aprendizado(id_frase, novo_peso, confianca_nova):
    with open(TABELA_APRENDIZADO, "a", newline="", encoding="utf-8") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        id_novo = contar_linhas_csv(TABELA_APRENDIZADO) + 1
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        escritor_csv.writerow([id_novo, id_frase, novo_peso, confianca_nova, data])

# Função para adicionar uma nova palavra à tabela de palavras (CSV)
def adicionar_palavra(palavra, peso):
    with open(TABELA_PALAVRAS, "a", newline="", encoding="utf-8") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerow([palavra, peso])

# Função para ler todas as linhas de uma tabela CSV
def ler_tabela(caminho):
    if not os.path.exists(caminho) or os.path.getsize(caminho) == 0:
        return []
    with open(caminho, "r", newline="", encoding="utf-8") as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        next(leitor_csv, None)  # Ignora o cabeçalho
        return list(leitor_csv)

# Função para criar a tabela "quemsou" se não existir (CSV)
def criar_tabela_quemsou():
    if not os.path.exists(TABELA_QUEMSOU):
        criar_tabela(TABELA_QUEMSOU, ["id", "atributo", "valor", "peso", "origem", "data_cadastro"])
        adicionar_quemsou("nome", "Jurema", 1, "sistema")
        adicionar_quemsou("idade", "23/02/2025 21:26", 1, "sistema")
        adicionar_quemsou("criador", "Lucas Ramalho", 1, "sistema")
        adicionar_quemsou("quem_sou", "uma IA", 1, "sistema")

# Função para adicionar um novo registro à tabela "quemsou" (CSV)
def adicionar_quemsou(atributo, valor, peso, origem):
    """Adiciona um novo registro à tabela "quemsou" se o atributo não existir."""
    registros = ler_quemsou()  # Lê todos os registros da tabela
    for linha in registros:
        if len(linha) >= 2 and linha[1] == atributo:
            # O atributo já existe, então não faz nada
            return

    # O atributo não existe, então adiciona um novo registro
    with open(TABELA_QUEMSOU, "a", newline="", encoding="utf-8") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        id_novo = contar_linhas_csv(TABELA_QUEMSOU) + 1
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        escritor_csv.writerow([id_novo, atributo, valor, peso, origem, data])

# Função para ler a tabela "quemsou" (CSV)
def ler_quemsou():
    return ler_tabela(TABELA_QUEMSOU)

# Função para buscar um atributo na tabela "quemsou" (CSV)
def buscar_quemsou(atributo):
    registros = ler_quemsou()
    for linha in registros:
        if len(linha) >= 3 and linha[1] == atributo:
            return linha[2]
    return None

# Função auxiliar para contar o número de linhas em um arquivo CSV
def contar_linhas_csv(caminho):
    if not os.path.exists(caminho) or os.path.getsize(caminho) == 0:
        return 0
    with open(caminho, "r", newline="", encoding="utf-8") as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        return sum(1 for linha in leitor_csv) - 1  # Subtrai 1 para ignorar o cabeçalho
    
# Função para adicionar letras à tabela do alfabeto
def adicionar_letra(letra, tipo, frequencia):
    with open(TABELA_ALFABETO, "a", newline="", encoding="utf-8") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerow([letra, tipo, frequencia])

# Adiciona as letras do alfabeto à tabela
alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
vogais = "AEIOU"
for letra in alfabeto:
    tipo = "vogal" if letra in vogais else "consoante"
    frequencia = 0  # Inicializa a frequência como 0
    adicionar_letra(letra, tipo, frequencia)