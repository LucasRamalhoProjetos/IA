# Jurema.py
import streamlit as st
from Neuronios import processar_texto, obter_historico_rede, obter_grafo_rede# Importe as funções do Neuronios.py
import matplotlib.pyplot as plt  # Importe a biblioteca matplotlib
import networkx as nx # Importe a biblioteca networkx

# Configuração da página
st.set_page_config(page_title="Chat com Jurema", page_icon="🤖")

# Título do chat
st.title("Chat com Jurema 🤖")

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de mensagem do usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Processa o texto usando a função processar_texto de Neuronios.py
    resposta = processar_texto(prompt)

    # Adiciona a resposta da IA ao histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.markdown(resposta)

# Sidebar para visualização da rede neural
st.sidebar.header("Visualização da Rede Neural")
historico_rede = obter_historico_rede()

# Gráfico de bolhas (grafo)
grafo = obter_grafo_rede()
if grafo:
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold")
    edge_labels = nx.get_edge_attributes(grafo, "peso")
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels)
    st.sidebar.pyplot(plt)
else:
    st.sidebar.write("Grafo da rede neural ainda não inicializado.")

# Gráficos de pesos e saída
if historico_rede and "pesos" in historico_rede and historico_rede["pesos"]:
    # Gráfico dos pesos
    fig_pesos, ax_pesos = plt.subplots()
    for i in range(len(historico_rede["pesos"][0])):
        ax_pesos.plot([p[i] for p in historico_rede["pesos"]], label=f"Peso {i}")
    ax_pesos.legend()
    ax_pesos.set_title("Evolução dos Pesos do Neurônio")
    ax_pesos.set_xlabel("Interações")
    ax_pesos.set_ylabel("Valor do Peso")
    st.sidebar.pyplot(fig_pesos)

    # Gráfico da saída
    fig_saida, ax_saida = plt.subplots()
    ax_saida.plot(historico_rede["saida"])
    ax_saida.set_title("Saída do Neurônio ao Longo do Tempo")
    ax_saida.set_xlabel("Interações")
    ax_saida.set_ylabel("Valor da Saída")
    st.sidebar.pyplot(fig_saida)
else:
    st.sidebar.write("Gráficos de pesos e saída ainda não inicializados.")


    