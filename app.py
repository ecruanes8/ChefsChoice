import streamlit as st
from login import login

login()

if st.session_state.get("authenticated"):
    st.write("✅ You're logged in!")
    st.page_link("pages/home_page.py", label="Go to Home", icon="🏠")
else:
    st.stop()
