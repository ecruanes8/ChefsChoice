import streamlit as st 
import streamlit_authenticator as stauth
import yaml 
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
st.title("Chef's Choice")

try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state.get('authentication_status'):
    authenticator.logout()
    st.sidebar.title(f'Welcome *{st.session_state.get("name")}*')
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')


page = st.sidebar.selectbox("Go to", ["Home", "Chatbot", "Preferences", "Recipe History"])
if page == "Home": 
    st.title("Chef's Choice Home")
    st.write("Here you can start exploring recipes or navigate to recently looked at tabs")
elif page == "Chatbot": 
    st.title("Chatbot")
    st.write("Chat with the chatbot to update, add or get new recipes!")
elif page == "Preferences": 
    st.title("Preferences")
elif page == "Recipe History": 
    st.title("Recipe History")
