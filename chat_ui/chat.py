import streamlit as st
import requests
from dotenv import load_dotenv
import os
load_dotenv()



server_url = os.getenv("SERVER_URL")

st.title("Chat App with FastAPI Backend")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Call FastAPI backend
        response = requests.post(
            server_url = os.getenv("SERVER_URL"),
            json= st.session_state.messages
        )
        assistant_response = response.json()["response"]
        st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
