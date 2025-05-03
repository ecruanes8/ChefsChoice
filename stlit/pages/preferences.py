import streamlit as st
import database 
# 🔐 Check login status
if not st.session_state.get("authenticated"):
    st.warning("Please log in to access the chatbot.")
    st.stop()

st.title("Preferences Page")
st.write(f"Welcome {st.session_state['name']}!")
st.write("Here you can find your set preferences. Feel free to update your preferences using the chatbot. ")

user_pref = database.get_user_preferences(st.session_state["user_id"])
history = database.get_user_history(st.session_state["user_id"])

data = {
    "Category": ["Preferences", "Intolerances", "Cuisine Preferences"], 
    "Values": [
        
    ]

}
