import streamlit as st
import os
import sys 
import yaml 
from yaml.loader import SafeLoader 
from dotenv import load_dotenv
from openai import OpenAI
import database 
import json 
from api_handler import search_recipe, search_recipe_by_ingredients


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
        if user_data:
            intro_message = (
                f"Hi again! I see your preferences include: {', '.join(user_data)}. "
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
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        system_prompt = """Extract recipe preferences from user input.
    Return JSON with these fields if available:
    - ingredients: list of strings
    - cuisine: string
    - diet: string
    - intolerances: list of strings
    - number: integer (number of recipes)

    If the user does not ask for recipes, reply normally.
    If user gives vague input (like 'what’s up'), return a friendly reply.
    """

        messages.insert(0, {"role": "system", "content": system_prompt})

        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages,
            temperature=0.7
        )

        reply = response.choices[0].message.content

        # Try parsing the reply as JSON
        try:
            params = json.loads(reply)

            # Update/ add preferences 
            preferences = []

            if "cuisine" in params and params["cuisine"]:
                preferences.append(params["cuisine"])
            if "diet" in params and params["diet"]:
                preferences.append(params["diet"])
            if "intolerances" in params and params["intolerances"]:
                preferences.extend(params["intolerances"])

            if preferences:
                database.update_user_preferences(user_id, preferences)
                print(f"✅ Preferences updated for {user_id}: {preferences}")

            recipes = search_recipe(
                query=None,
                cuisine=params.get("cuisine"),
                diet=params.get("diet"),
                intolerances=",".join(params.get("intolerances", [])),
                number=params.get("number", 3)
            )
            if recipes["results"]:
                formatted = "\n".join([f"- {r['title']}" for r in recipes["results"]])
                final_response = f"Here are some recipes I found:\n\n{formatted}"
            else:
                final_response = "Sorry, I couldn't find any matching recipes."

        except Exception as e: 
            # Fallback: treat the response as a normal chat reply
            print(f"Error {e}")
            final_response = reply
        st.markdown("This was the final_response")
        st.markdown(final_response)

    st.session_state.messages.append({"role": "assistant", "content": final_response})
