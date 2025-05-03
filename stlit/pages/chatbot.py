import streamlit as st
import os
import sys 
import yaml 
from yaml.loader import SafeLoader 
from dotenv import load_dotenv
from openai import OpenAI
import database 

# 🔐 Check login status
if not st.session_state.get("authenticated"):
    st.warning("Please log in to access the chatbot.")
    st.stop()

# Load environment variables
load_dotenv()

# Set up OpenAI
openai_api_key = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=openai_api_key)
# Load authentication config
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.yaml"))
with open(config_path) as file:
    config = yaml.load(file, Loader=SafeLoader)
# 🧠 Set model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# 👤 Get user info
user_id = st.session_state["username"]
name = st.session_state["name"]

# 👋 Sidebar greeting
st.sidebar.success(f"Welcome, {name}!")
if st.sidebar.button("Logout"):
    for key in ["authenticated", "username", "name"]:
        st.session_state.pop(key, None)
    st.rerun()

# 💬 Title
st.title("Recipe Chatbot")

# 📦 Load preferences or initialize user
if "messages" not in st.session_state:
    user_data = database.get_user_preferences(user_id)

    if not user_data:
        database.add_user(user_id)
        intro_message = (
            "Hi! I am here to help build your recipe history based on your preferences, "
            "ingredients, and any intolerances."
        )
    else:
        prefs = user_data.get("preferences", [])
        if prefs:
            intro_message = (
                f"Hi again! I see your preferences include: {', '.join(prefs)}. "
                "Would you like to update them or get recipe suggestions?"
            )
        else:
            intro_message = (
                "Hi! You haven’t set any preferences yet. "
                "Please tell me your ingredients, preferences, or dietary needs!"
            )

    st.session_state.messages = [{"role": "assistant", "content": intro_message}]

# 💬 Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🧠 Handle user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})