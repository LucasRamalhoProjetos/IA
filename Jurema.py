# Jurema.py
import streamlit as st
from Neuronios import processar_texto, obter_historico_rede, obter_grafo_rede# Importe as funções do Neuronios.py
import matplotlib.pyplot as plt  # Importe a biblioteca matplotlib
import networkx as nx # Importe a biblioteca networkx
import plotly.graph_objects as go  # Importe o Plotly corretamente

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

# Gráfico de bolhas (grafo) com Plotly
grafo = obter_grafo_rede()
if grafo:
    pos = nx.spring_layout(grafo)

    # Criação das arestas para o Plotly
    edge_x = []
    edge_y = []
    edge_text = []  # Lista para armazenar o texto das arestas
    for edge in grafo.edges(data=True):  # Obtém os dados das arestas
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        peso = edge[2].get('peso', 0)  # Obtém o peso da aresta
        edge_text.append(f"Peso: {peso:.3f}")  # Formata o peso com 3 casas decimais

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='text',  # Habilita o texto ao passar o mouse
        mode='lines',
        text=edge_text  # Usa o texto formatado para as arestas
    )

    # Criação dos nós para o Plotly
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    
    # Suponha que o neurônio 0 seja a entrada e o neurônio N-1 seja a saída
    entrada_node = 0
    saida_node = len(grafo.nodes()) - 1

    for node in grafo.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        grau = grafo.degree(node)
        node_text.append(f"Neurônio {node}<br>Grau: {grau}")
        
        # Define a cor do nó com base se é entrada ou saída
        if node == entrada_node:
            node_colors.append('red')
        elif node == saida_node:
            node_colors.append('green')
        else:
            node_colors.append('skyblue')

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=node_colors,
            size=20,
            line_width=2),
        text=node_text)

    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Rede Neural",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    st.sidebar.plotly_chart(fig)

else:
    st.sidebar.write("Grafo da rede neural ainda não inicializado.")

# Gráficos de pesos e saída com Plotly
if historico_rede and "pesos" in historico_rede and historico_rede["pesos"]:
    # Gráfico dos pesos com Plotly
    fig_pesos = go.Figure()
    for i in range(len(historico_rede["pesos"][0])):
        fig_pesos.add_trace(go.Scatter(y=[p[i] for p in historico_rede["pesos"]], mode='lines', name=f"Peso {i}"))
    fig_pesos.update_layout(title="Evolução dos Pesos do Neurônio", xaxis_title="Interações", yaxis_title="Valor do Peso")
    st.sidebar.plotly_chart(fig_pesos)

    # Gráfico da saída com Plotly
    fig_saida = go.Figure(data=go.Scatter(y=historico_rede["saida"], mode='lines'))
    fig_saida.update_layout(title="Saída do Neurônio ao Longo do Tempo", xaxis_title="Interações", yaxis_title="Valor da Saída")
    st.sidebar.plotly_chart(fig_saida)
else:
    st.sidebar.write("Gráficos de pesos e saída ainda não inicializados.")


    