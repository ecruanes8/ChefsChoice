import streamlit as st
import pandas as pd 
import numpy as np
import database 
# 🔐 Check login status
if not st.session_state.get("authenticated"):
    st.warning("Please log in to access the chatbot.")
    st.stop()

st.title("Preferences Page")
st.write(f"Welcome {st.session_state['name']}!")
st.write("Here you can find your set preferences. Feel free to update your preferences using the chatbot. ")

if "username" not in st.session_state:
    st.warning("Please log in to access your preferences.")
    st.stop()

user_pref = database.get_user_preferences(st.session_state["username"])
history = database.get_user_history(st.session_state["username"])
database.print_all_users()
print(user_pref)
# database stuff 
#df = pd.DataFrame()
if user_pref:
    st.header("🍽️ Your Preferences")
    st.write(user_pref)
else:
    st.info("No preferences found. You can add some below.")


