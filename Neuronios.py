import os
import ollama  # Biblioteca para interagir com o Ollama
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
    TABELA_SENSACOES, 
    TABELA_CONTEXTO, 
    TABELA_APRENDIZADO, 
    TABELA_PALAVRAS,
    criar_tabela_quemsou, 
    buscar_quemsou, 
    adicionar_quemsou
)

def perguntar_ollama(texto):
    """Pergunta ao Ollama, retorna a resposta gerada pela IA e preenche as tabelas com os dados relevantes."""
    try:
        # Consulta o Ollama para obter a resposta
        resposta = ollama.chat(model="llama3", messages=[{"role": "user", "content": texto}])
        resposta_ia = resposta["message"]["content"]

        # Adiciona a frase do usuário à tabela de frases (peso padrão 0.5, origem "humano")
        id_frase = adicionar_frase(texto, 0.5, "humano")

        # Adiciona a resposta da IA à tabela de respostas (confiança padrão 0.5)
        adicionar_resposta(id_frase, resposta_ia, 0.5)

        # Adiciona um contexto à tabela de contexto (resposta sugerida é a própria resposta da IA)
        adicionar_contexto(id_frase, resposta_ia)

        # Adiciona uma sensação padrão à tabela de sensações (emoção "neutro", valor 0.5)
        adicionar_sensacao("neutro", 0.5)

        # Adiciona um registro de aprendizado à tabela de aprendizado (novo_peso 0.5, confianca_nova 0.5)
        adicionar_aprendizado(id_frase, 0.5, 0.5)

        # Adiciona palavras da frase do usuário à tabela de palavras (peso padrão 0.5)
        palavras = texto.split()
        for palavra in palavras:
            adicionar_palavra(palavra, 0.5)

        return resposta_ia

    except Exception as e:
        return f"Erro ao consultar o Ollama: {str(e)}"

def processar_texto(texto, origem="humano"):
    """Processa a entrada do usuário, busca resposta na base e consulta o Ollama se necessário."""
    
    # Cria a tabela "quemsou" se não existir
    criar_tabela_quemsou()
    
    # Verifica se a pergunta é sobre a Jurema
    if "quem é você" in texto.lower() or "quem sou eu" in texto.lower() or "fale sobre você" in texto.lower():
        # Busca informações na tabela "quemsou"
        nome = buscar_quemsou("nome")
        idade = buscar_quemsou("idade")
        criador = buscar_quemsou("criador")
        quem_sou = buscar_quemsou("quem_sou")
        
        if nome and idade and criador and quem_sou:
            return f"Eu sou {nome}, {quem_sou}. Fui criada por {criador} em {idade}."
        else:
            return "Desculpe, não tenho informações suficientes sobre mim."
    
    # Verifica se o arquivo de frases existe e não está vazio
    if not os.path.exists(TABELA_FRASES) or os.path.getsize(TABELA_FRASES) == 0:
        id_frase = adicionar_frase(texto, 0.5, origem)
    else:
        frases = ler_tabela(TABELA_FRASES)
        id_frase = None
        peso = 0.5  # Padrão neutro caso a frase não exista

        for linha in frases:
            if len(linha) >= 2 and linha[1] == texto:  # Verifica se linha[1] existe
                id_frase = int(linha[0])
                peso = float(linha[2])
                break

        if id_frase is None:
            id_frase = adicionar_frase(texto, peso, origem)

    # Verifica se o arquivo de respostas existe e não está vazio
    if not os.path.exists(TABELA_RESPOSTAS) or os.path.getsize(TABELA_RESPOSTAS) == 0:
        melhor_resposta = None
    else:
        respostas = ler_tabela(TABELA_RESPOSTAS)
        melhor_resposta = None
        maior_confianca = 0

        for linha in respostas:
            if len(linha) >= 4 and int(linha[1]) == id_frase:  # Verifica se linha[1] e linha[3] existem
                confianca = float(linha[3])
                if confianca > maior_confianca:
                    melhor_resposta = linha[2]
                    maior_confianca = confianca

    # Se não houver resposta conhecida, perguntar ao Ollama
    if melhor_resposta is None:
        print("Perguntando ao Ollama...")
        melhor_resposta = perguntar_ollama(texto)

    return melhor_resposta