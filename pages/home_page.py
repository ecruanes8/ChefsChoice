import streamlit as st

if not st.session_state.get("authenticated"):
    st.warning("Please log in first.")
    st.stop()
st.title("HOME PAGE")
st.write(f"Welcome {st.session_state['name']}!")
st.write("Refer to the chatbot or preferences tab to find some recipes!")

