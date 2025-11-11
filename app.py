import os
import time
import streamlit as st
import requests
from config.config import Config
from utils.styling import load_css

load_css()

BASE_URL = "http://fastapi:8000" if os.environ.get("DOCKER") else "http://localhost:8000"

st.set_page_config(page_title="MD Assistant", page_icon=Config.PAGE_ICON, layout="wide")

st.html("<h1>MD Assistant</h1>")
st.write("Ask questions related to MD Company Policy.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "user":
        st.html(f"<div class='chat-bubble user-bubble'>{message['content']}</div>")
    else:
        st.html(f"<div class='chat-bubble assistant-bubble'>{message['content']}</div>")

if prompt := st.chat_input("Type your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.html(f"<div class='chat-bubble user-bubble'>{prompt}</div>")

    with st.spinner("Generating a response..."):
        start_time = time.time()
        try:
            response = requests.post(f"{BASE_URL}/chat", json={"question": prompt}, timeout=300)
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.session_state.messages.append({"role": "assistant", "content": answer})
                end_time = time.time()
                st.html(f"<div class='chat-bubble assistant-bubble'>{answer}</div>")
                st.caption(f"({end_time - start_time:.2f} s)")
            else:
                st.error(f"API error: {response.status_code} - {response.text}")
                st.session_state.messages.pop()
        except requests.exceptions.RequestException as e:
            st.error(f"API connection failed: {e}")
            st.session_state.messages.pop()

st.html("<div class='footer'>©2025 Rifqi Anshari Rasyid.</div>")
