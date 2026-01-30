import streamlit as st
import requests

API = "http://127.0.0.1:8000"

if st.session_state.get("role") != "admin":
    st.warning("Admin access only")
    st.stop()

st.title("Admin Dashboard")

file = st.file_uploader("Upload PDF", type=["pdf"])

if st.button("Upload"):
    if file:
        r = requests.post(f"{API}/upload", files={"file": file})
        st.success(r.json())


st.subheader("Stats")

if st.button("Refresh"):
    r = requests.get(f"{API}/stats")
    st.json(r.json())
