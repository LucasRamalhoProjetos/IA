# Jurema.py
import streamlit as st
from Neuronios import processar_texto  # Importa a função processar_texto

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