import os
from datetime import datetime

# Cria a pasta "Tabelas" se não existir
if not os.path.exists("Tabelas"):
    os.makedirs("Tabelas")

# Caminhos para os arquivos das tabelas
TABELA_FRASES = "Tabelas/frases.txt"
TABELA_SENSACOES = "Tabelas/sensacoes.txt"
TABELA_CONTEXTO = "Tabelas/contexto.txt"
TABELA_RESPOSTAS = "Tabelas/respostas.txt"
TABELA_APRENDIZADO = "Tabelas/aprendizado.txt"
TABELA_PALAVRAS = "Tabelas/palavras.txt"
TABELA_QUEMSOU = "Tabelas/quemsou.txt"

# Função para criar uma tabela se não existir
def criar_tabela(caminho, cabecalho):
    if not os.path.exists(caminho):
        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(cabecalho + "\n")

# Cria as tabelas com seus cabeçalhos
criar_tabela(TABELA_FRASES, "id\tfrase\tpeso\torigem\tdata_cadastro")
criar_tabela(TABELA_SENSACOES, "id\temocao\tvalor\tdata_atualizacao")
criar_tabela(TABELA_CONTEXTO, "id\tid_frase\tresposta_sugerida\tdata")
criar_tabela(TABELA_RESPOSTAS, "id\tid_frase\tresposta\tconfianca")
criar_tabela(TABELA_APRENDIZADO, "id\tid_frase\tnovo_peso\tconfianca_nova\tdata")
criar_tabela(TABELA_PALAVRAS, "palavra\tpeso")
criar_tabela(TABELA_QUEMSOU, "id\tatributo\tvalor\tpeso\torigem\tdata_cadastro")

# Função para adicionar uma nova frase à tabela de frases
def adicionar_frase(frase, peso, origem):
    with open(TABELA_FRASES, "a", encoding="utf-8") as arquivo:
        # Gera o próximo ID
        if os.path.getsize(TABELA_FRASES) == 0:
            id_novo = 1
        else:
            id_novo = sum(1 for _ in open(TABELA_FRASES))  # Conta as linhas existentes
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        arquivo.write(f"{id_novo}\t{frase}\t{peso}\t{origem}\t{data}\n")
    return id_novo  # Retorna o ID gerado

# Função para adicionar uma nova sensação à tabela de sensações
def adicionar_sensacao(emocao, valor):
    with open(TABELA_SENSACOES, "a", encoding="utf-8") as arquivo:
        # Gera o próximo ID
        if os.path.getsize(TABELA_SENSACOES) == 0:
            id_novo = 1
        else:
            id_novo = sum(1 for _ in open(TABELA_SENSACOES))
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        arquivo.write(f"{id_novo}\t{emocao}\t{valor}\t{data}\n")

# Função para adicionar um novo contexto à tabela de contexto
def adicionar_contexto(id_frase, resposta_sugerida):
    with open(TABELA_CONTEXTO, "a", encoding="utf-8") as arquivo:
        # Gera o próximo ID
        if os.path.getsize(TABELA_CONTEXTO) == 0:
            id_novo = 1
        else:
            id_novo = sum(1 for _ in open(TABELA_CONTEXTO))
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        arquivo.write(f"{id_novo}\t{id_frase}\t{resposta_sugerida}\t{data}\n")

# Função para adicionar uma nova resposta à tabela de respostas
def adicionar_resposta(id_frase, resposta, confianca):
    with open(TABELA_RESPOSTAS, "a", encoding="utf-8") as arquivo:
        # Gera o próximo ID
        if os.path.getsize(TABELA_RESPOSTAS) == 0:
            id_novo = 1
        else:
            id_novo = sum(1 for _ in open(TABELA_RESPOSTAS))
        arquivo.write(f"{id_novo}\t{id_frase}\t{resposta}\t{confianca}\n")

# Função para adicionar um novo registro de aprendizado
def adicionar_aprendizado(id_frase, novo_peso, confianca_nova):
    with open(TABELA_APRENDIZADO, "a", encoding="utf-8") as arquivo:
        # Gera o próximo ID
        if os.path.getsize(TABELA_APRENDIZADO) == 0:
            id_novo = 1
        else:
            id_novo = sum(1 for _ in open(TABELA_APRENDIZADO))
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        arquivo.write(f"{id_novo}\t{id_frase}\t{novo_peso}\t{confianca_nova}\t{data}\n")

# Função para adicionar uma nova palavra à tabela de palavras
def adicionar_palavra(palavra, peso):
    with open(TABELA_PALAVRAS, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{palavra}\t{peso}\n")

# Função para ler todas as linhas de uma tabela
def ler_tabela(caminho):
    if not os.path.exists(caminho) or os.path.getsize(caminho) == 0:
        return []  # Retorna uma lista vazia se o arquivo não existir ou estiver vazio
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return [linha.strip().split("\t") for linha in arquivo.readlines()[1:]]  # Ignora o cabeçalho

# Função para criar a tabela "quemsou" se não existir
def criar_tabela_quemsou():
    if not os.path.exists(TABELA_QUEMSOU):
        with open(TABELA_QUEMSOU, "w", encoding="utf-8") as arquivo:
            arquivo.write("id\tatributo\tvalor\tpeso\torigem\tdata_cadastro\n")
        
        # Adiciona os dados iniciais
        adicionar_quemsou("nome", "Jurema", 1, "sistema")
        adicionar_quemsou("idade", "23/02/2025 21:26", 1, "sistema")
        adicionar_quemsou("criador", "Lucas Ramalho", 1, "sistema")
        adicionar_quemsou("quem_sou", "uma IA", 1, "sistema")

# Função para adicionar um novo registro à tabela "quemsou"
def adicionar_quemsou(atributo, valor, peso, origem):
    with open(TABELA_QUEMSOU, "a", encoding="utf-8") as arquivo:
        # Gera o próximo ID
        if os.path.getsize(TABELA_QUEMSOU) == 0:
            id_novo = 1
        else:
            id_novo = sum(1 for _ in open(TABELA_QUEMSOU))  # Conta as linhas existentes
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        arquivo.write(f"{id_novo}\t{atributo}\t{valor}\t{peso}\t{origem}\t{data}\n")

# Função para ler a tabela "quemsou"
def ler_quemsou():
    if not os.path.exists(TABELA_QUEMSOU) or os.path.getsize(TABELA_QUEMSOU) == 0:
        return []  # Retorna uma lista vazia se o arquivo não existir ou estiver vazio
    with open(TABELA_QUEMSOU, "r", encoding="utf-8") as arquivo:
        return [linha.strip().split("\t") for linha in arquivo.readlines()[1:]]  # Ignora o cabeçalho

# Função para buscar um atributo na tabela "quemsou"
def buscar_quemsou(atributo):
    registros = ler_quemsou()
    for linha in registros:
        if len(linha) >= 3 and linha[1] == atributo:  # Verifica se o atributo existe
            return linha[2]  # Retorna o valor do atributo
    return None  # Retorna None se o atributo não for encontrado