import streamlit as st

import streamlit as st

if not st.session_state.get("authenticated"):
    st.warning("Please log in first.")
    st.stop()
st.title("HOME PAGE")
st.write(f"Welcome {st.session_state['name']}!")

