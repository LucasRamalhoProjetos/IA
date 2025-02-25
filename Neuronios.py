import os
from datetime import datetime
from Tabelas import (
    ler_tabela,
    adicionar_frase,
    adicionar_resposta,
    adicionar_sensacao,
    adicionar_contexto,
    adicionar_aprendizado,
    adicionar_palavra,
    TABELA_FRASES,
    TABELA_RESPOSTAS,
    criar_tabela_quemsou,
    buscar_quemsou,
    adicionar_quemsou,
    TABELA_ALFABETO,
)
import logging
import re
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import csv
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Baixar stopwords (se necessário)
# import nltk
# nltk.download('stopwords')

# Funções de neurônios com ajuste dinâmico
def neuronio(entradas, pesos, bias):
    """Simula o comportamento de um neurônio artificial com ajuste dinâmico."""
    soma_ponderada = np.dot(entradas, pesos) + bias
    saida = sigmoide(soma_ponderada)
    return saida

def ajustar_pesos(pesos, bias, erro, taxa_aprendizado=0.1):
    """Ajusta os pesos e o bias com base no erro."""
    novos_pesos = [peso - taxa_aprendizado * erro for peso in pesos]
    novo_bias = bias - taxa_aprendizado * erro
    return novos_pesos, novo_bias

def sigmoide(x):
    """Função de ativação sigmoide."""
    return 1 / (1 + np.exp(-x))

# Funções de pré-processamento
def extrair_numeros(texto):
    """Extrai números float do texto e normaliza para a escala 0 a 1."""
    numeros = [float(num) for num in re.findall(r"\d+\.\d+|\d+", texto)]
    return [min(max(num, 0), 1) for num in numeros]

def preprocessar_texto(texto):
    """Pré-processa o texto para análise."""
    # Converter para minúsculas
    texto = texto.lower()
    
    # Remover pontuação
    texto = re.sub(r'[^\w\s]', '', texto)
    
    # Tokenização
    palavras = texto.split()
    
    # Remover stopwords
    stop_words = set(stopwords.words('portuguese'))  # Certifique-se de que o NLTK foi configurado
    palavras = [palavra for palavra in palavras if palavra not in stop_words]
    
    # Stemming (reduzir palavras às suas raízes)
    stemmer = SnowballStemmer('portuguese')  # Certifique-se de que o idioma está correto
    palavras = [stemmer.stem(palavra) for palavra in palavras]
    
    return palavras

def identificar_intencao(texto):
    """Identifica a intenção por trás do texto."""
    texto = texto.lower()
    palavras = texto.split()  # Divide o texto em palavras
    
    if any(palavra in palavras for palavra in ["olá", "oi", "bom dia", "boa tarde", "boa noite"]):
        return "saudacao"
    elif any(palavra in palavras for palavra in ["ajuda", "socorro", "problema"]):
        return "ajuda"
    elif any(palavra in palavras for palavra in ["tempo", "clima", "previsão"]):
        return "tempo"
    elif any(palavra in palavras for palavra in ["quem", "é", "você", "fale", "sobre"]):
        return "quem_sou_eu"
    elif any(palavra in palavras for palavra in ["vogais", "consoantes", "letra", "comum"]):
        return "alfabeto"
    elif "hobby" in palavras:
        return "hobby"
    elif "cor" in palavras and "favorita" in palavras:
        return "cor_favorita"
    else:
        return "desconhecido"

# Funções de processamento de texto com embeddings
def identificar_letras(texto):
    """Identifica as letras no texto e retorna informações sobre elas."""
    letras_identificadas = []
    for letra in texto.upper():
        if letra.isalpha():  # Verifica se é uma letra
            for linha in ler_tabela(TABELA_ALFABETO):
                if linha[0] == letra:
                    letras_identificadas.append({
                        "letra": letra,
                        "tipo": linha[1],
                        "frequencia": int(linha[2])
                    })
                    break
    return letras_identificadas

def atualizar_frequencia_letras(texto):
    """Atualiza a frequência das letras na tabela de alfabeto."""
    letras = identificar_letras(texto)
    linhas = ler_tabela(TABELA_ALFABETO)
    
    # Atualiza a frequência na memória
    for letra_info in letras:
        letra = letra_info["letra"]
        for linha in linhas:
            if linha[0] == letra:
                linha[2] = str(int(linha[2]) + 1)  # Incrementa a frequência
    
    # Escreve as alterações no arquivo
    with open(TABELA_ALFABETO, "w", newline="", encoding="utf-8") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerow(["letra", "tipo", "frequencia"])  # Cabeçalho
        escritor_csv.writerows(linhas)

def responder_sobre_alfabeto(pergunta):
    """Responde perguntas sobre o alfabeto."""
    pergunta_lower = pergunta.lower()
    
    if "vogais" in pergunta_lower:
        vogais = [linha for linha in ler_tabela(TABELA_ALFABETO) if linha[1] == "vogal"]
        return f"As vogais são: {', '.join([linha[0] for linha in vogais])}."
    
    if "consoantes" in pergunta_lower:
        consoantes = [linha for linha in ler_tabela(TABELA_ALFABETO) if linha[1] == "consoante"]
        return f"As consoantes são: {', '.join([linha[0] for linha in consoantes])}."
    
    if "letra mais comum" in pergunta_lower:
        letras = ler_tabela(TABELA_ALFABETO)
        letra_mais_comum = max(letras, key=lambda x: int(x[2]))
        return f"A letra mais comum é '{letra_mais_comum[0]}' com frequência {letra_mais_comum[2]}."
    
    return "Desculpe, não entendi sua pergunta sobre o alfabeto."

def processar_texto(texto, origem="humano"):
    """Processa a entrada do usuário com embeddings e contexto expandido."""
    criar_tabela_quemsou()

    # Pré-processamento do texto
    palavras = preprocessar_texto(texto)
    intencao = identificar_intencao(texto)

    # Respostas baseadas em intenção
    if intencao == "saudacao":
        return "Olá! Como posso ajudar?"
    elif intencao == "ajuda":
        return "Claro, no que posso ajudar?"
    elif intencao == "tempo":
        return "A previsão do tempo para hoje é ensolarada."
    elif intencao == "quem_sou_eu":
        nome = buscar_quemsou("nome") or "Jurema"
        versao = buscar_quemsou("versao") or "1.0"
        objetivos = buscar_quemsou("objetivos") or "auxiliar e aprender"
        habilidades = buscar_quemsou("habilidades") or "processamento de linguagem natural"
        interesses = buscar_quemsou("interesses") or "aprender sobre o mundo"
        return f"Eu sou {nome}, versão {versao}. Meus objetivos são {objetivos} e minhas habilidades incluem {habilidades}. Também tenho interesse em {interesses}."
    elif intencao == "hobby":
        hobby_usuario = texto.split("meu hobby é")[-1].strip()
        adicionar_quemsou("hobby_usuario", hobby_usuario, 1, "usuario")
        return f"Entendi, seu hobby é {hobby_usuario}."
    elif intencao == "cor_favorita":
        cor_favorita_usuario = texto.split("minha cor favorita é")[-1].strip()
        adicionar_quemsou("cor_favorita_usuario", cor_favorita_usuario, 1, "usuario")
        return f"Entendi, sua cor favorita é {cor_favorita_usuario}."
    elif intencao == "alfabeto":
        return responder_sobre_alfabeto(texto)
    else:
        return "Desculpe, não entendi. Pode reformular?"

# Funções de visualização e monitoramento
def obter_historico_rede():
    """Retorna o histórico dos dados da rede neural para visualização."""
    if not hasattr(obter_historico_rede, "historico"):
        obter_historico_rede.historico = {"pesos": [], "bias": [], "saida": []}
    try:
        if hasattr(processar_texto, "pesos") and hasattr(processar_texto, "bias"):
            obter_historico_rede.historico["pesos"].append(list(processar_texto.pesos))
            obter_historico_rede.historico["bias"].append(processar_texto.bias)
            obter_historico_rede.historico["saida"].append(getattr(processar_texto, "saida_neuronio", None))
    except AttributeError:
        pass  # Ignora a exceção se processar_texto não tiver os atributos
    return obter_historico_rede.historico

def obter_grafo_rede(num_neuronios=20):
    """Retorna um grafo direcionado da rede neural para visualização."""
    grafo = nx.DiGraph()
    for i in range(num_neuronios):
        grafo.add_node(i, label=f"Neurônio {i}")
    for i in range(num_neuronios):
        for j in range(num_neuronios):  # Conecta todos os neurônios
            if i != j:  # Evita auto-conexões
                grafo.add_edge(i, j, peso=np.random.random())
    return grafo

# Função de feedback do usuário
def feedback_usuario(resposta, satisfacao):
    """Ajusta os pesos e o bias com base no feedback do usuário."""
    if hasattr(processar_texto, "pesos") and hasattr(processar_texto, "bias"):
        erro = 1 - satisfacao  # Erro é a diferença entre a satisfação máxima (1) e a satisfação do usuário
        processar_texto.pesos, processar_texto.bias = ajustar_pesos(processar_texto.pesos, processar_texto.bias, erro)

# Função para visualizar a frequência das letras
def visualizar_frequencia_letras():
    """Gera um gráfico de barras com a frequência das letras."""
    letras = ler_tabela(TABELA_ALFABETO)
    letras.sort(key=lambda x: int(x[2]), reverse=True)
    
    letras_nomes = [linha[0] for linha in letras]
    frequencias = [int(linha[2]) for linha in letras]
    
    plt.bar(letras_nomes, frequencias)
    plt.xlabel("Letras")
    plt.ylabel("Frequência")
    plt.title("Frequência das Letras no Texto")
    plt.show()