import streamlit as st
import requests
import uuid


st.title("Chat App with FastAPI Backend")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    st.rerun()

# Display current session ID
# st.sidebar.markdown(f"**Session ID:** {st.session_state.session_id[:8]}...")

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
            f"{st.secrets['SERVER_URL']}/chat",
            json={
                "message": prompt,
                "session_id": st.session_state.session_id
            }
        )
        assistant_response = response.json()["response"]
        st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
