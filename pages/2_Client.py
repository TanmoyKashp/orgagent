import streamlit as st
import requests

API = "http://127.0.0.1:8000"

if st.session_state.get("role") != "user":
    st.warning("User access only")
    st.stop()

st.title("OrgAgent Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

query = st.chat_input("Ask something...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.chat_message("user").write(query)

    r = requests.post(f"{API}/chat", params={"query": query})
    answer = r.json()["response"]

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
