import streamlit as st
from auth import login

st.set_page_config(page_title="OrgAgent", layout="wide")

# ----------------------
# Session init
# ----------------------
if "role" not in st.session_state:
    st.session_state.role = None


# ----------------------
# LOGIN PAGE
# ----------------------
if st.session_state.role is None:
    st.title("OrgAgent Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = login(username, password)

        if role:
            st.session_state.role = role
            st.rerun()
        else:
            st.error("Invalid credentials")


# ----------------------
# AFTER LOGIN
# ----------------------
else:
    col1, col2 = st.columns([8, 1])

    with col1:
        st.success(f"Logged in as: {st.session_state.role}")

    with col2:
        if st.button("Logout"):
            st.session_state.role = None
            st.rerun()

    st.write("Select a page from sidebar →")
