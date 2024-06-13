import streamlit as st
from streamlit_chat import message
from langchain_community.llms import Ollama
from datetime import datetime

now = str(datetime.now())
st.title("★선녀보살 무료사주★")
st.image("image.png", width=500)
message("무엇이 궁금해 나를 찾아왔는가?")

llm = Ollama(model="llama3-ko:latest")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("물어보거라!"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("대답 생성 중..."):
        st.write(llm.invoke(prompt, stop=['<|eot_id|>']))