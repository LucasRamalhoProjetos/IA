import os
import ollama
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
    adicionar_quemsou
)
import logging
import re
import numpy as np  # Importe a biblioteca NumPy
import matplotlib.pyplot as plt  # Importe a biblioteca matplotlib
import networkx as nx  # Importe a biblioteca networkx

# Funções de neurônios
def neuronio(entradas, pesos, bias):
    """Simula o comportamento de um neurônio artificial."""
    soma_ponderada = np.dot(entradas, pesos) + bias
    saida = sigmoide(soma_ponderada)
    return saida

def sigmoide(x):
    """Função de ativação sigmoide."""
    return 1 / (1 + np.exp(-x))

# Funções de pré-processamento
def extrair_numeros(texto):
    """Extrai números float do texto e normaliza para a escala 0 a 1."""
    numeros = [float(num) for num in re.findall(r"\d+\.\d+|\d+", texto)]
    return [min(max(num, 0), 1) for num in numeros]

# Funções de interação com o Ollama
def perguntar_ollama(texto):
    """Pergunta ao Ollama e armazena dados da resposta."""
    if not texto.strip():
        return "Erro: Texto da pergunta está vazio."

    try:
        logging.info(f"Perguntando ao Ollama: {texto}")

        resposta = ollama.chat(model="llama3", messages=[{"role": "user", "content": texto}])
        resposta_ia = resposta.get("message", {}).get("content", "").strip()
        if not resposta_ia:
            return "Erro: Resposta da IA está vazia."

        avaliacao = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": f"Avalie a resposta: '{resposta_ia}'. Dê confiança (0 a 1) e peso (0 a 1)."}]
        )
        avaliacao_ia = avaliacao.get("message", {}).get("content", "").strip()

        valores = extrair_numeros(avaliacao_ia)
        confianca = valores[0] if len(valores) > 0 else 0.5
        peso = valores[1] if len(valores) > 1 else 0.5

        logging.info(f"Resposta: {resposta_ia} | Confiança: {confianca} | Peso: {peso}")

        id_frase = adicionar_frase(texto, peso, "humano")
        adicionar_resposta(id_frase, resposta_ia, confianca)
        adicionar_contexto(id_frase, resposta_ia)
        adicionar_sensacao("neutro", peso)
        adicionar_aprendizado(id_frase, peso, confianca)

        for palavra in set(texto.lower().split()):
            adicionar_palavra(palavra, peso)

        return resposta_ia
    except Exception as e:
        logging.error(f"Erro ao consultar o Ollama: {str(e)}", exc_info=True)
        return f"Erro ao consultar o Ollama: {str(e)}"

# Funções de processamento de texto
def processar_texto(texto, origem="humano"):
    """Processa a entrada do usuário, busca resposta na base, adapta-se e consulta o Ollama se necessário."""
    criar_tabela_quemsou()

    texto_lower = texto.lower()

    # Resposta "Quem Sou Eu?" expandida e personalizada
    if any(pergunta in texto_lower for pergunta in ["quem é você", "quem sou eu", "fale sobre você"]):
        nome = buscar_quemsou("nome") or "Jurema"
        versao = buscar_quemsou("versao") or "1.0"
        objetivos = buscar_quemsou("objetivos") or "auxiliar e aprender"
        habilidades = buscar_quemsou("habilidades") or "processamento de linguagem natural"
        interesses = buscar_quemsou("interesses") or "aprender sobre o mundo"
        return f"Eu sou {nome}, versão {versao}. Meus objetivos são {objetivos} e minhas habilidades incluem {habilidades}. Também tenho interesse em {interesses}."

    # Aprendizado de novos atributos
    if "meu hobby é" in texto_lower:
        hobby_usuario = texto.split("meu hobby é")[-1].strip()
        adicionar_quemsou("hobby_usuario", hobby_usuario, 1, "usuario")
        return f"Entendi, seu hobby é {hobby_usuario}."

    if "minha cor favorita é" in texto_lower:
        cor_favorita_usuario = texto.split("minha cor favorita é")[-1].strip()
        adicionar_quemsou("cor_favorita_usuario", cor_favorita_usuario, 1, "usuario")
        return f"Entendi, sua cor favorita é {cor_favorita_usuario}."

    # Memória de conversação (simples - pode ser expandida)
    if hasattr(processar_texto, "ultima_pergunta"):
        if "sim" in texto_lower:
            return "Ótimo!"
        del processar_texto.ultima_pergunta

    # Perguntas de acompanhamento
    if "você gosta de" in texto_lower:
        processar_texto.ultima_pergunta = texto
        return "Sim, gosto. E você?"

    # Busca de respostas na base de dados (usando neurônio)
    frases = {linha[1]: int(linha[0]) for linha in ler_tabela(TABELA_FRASES)}
    id_frase = frases.get(texto, adicionar_frase(texto, 0.5, origem))

    respostas = {}
    for linha in ler_tabela(TABELA_RESPOSTAS):
        if len(linha) >= 4:
            try:
                respostas[int(linha[1])] = (linha[2], float(linha[3]))
            except ValueError:
                print(f"Erro: Valor inválido encontrado na linha: {linha}")
        else:
            print(f"Aviso: Linha incompleta encontrada: {linha}")

    melhor_resposta, maior_confianca = respostas.get(id_frase, (None, 0))

    # Uso da rede neural para decidir se usa a resposta da base ou o Ollama
    entradas = [len(texto), maior_confianca, id_frase]  # Entradas fictícias
    pesos = [0.1, 0.2, 0.3]  # Pesos aleatórios
    bias = 0.5  # Bias aleatório
    saida_neuronio = neuronio(entradas, pesos, bias)

    processar_texto.pesos = pesos  # Armazena os pesos
    processar_texto.bias = bias    # Armazena o bias
    processar_texto.saida_neuronio = saida_neuronio # Armazena a saída

    if saida_neuronio > 0.5:  # Limiar de ativação
        if melhor_resposta:
            return melhor_resposta
        else:
            return perguntar_ollama(texto)
    else:
        return perguntar_ollama(texto)

# Funções de visualização
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

