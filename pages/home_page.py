import streamlit as st 
import streamlit_authenticator as stauth
import yaml 
from yaml.loader import SafeLoader 

# re-load login 
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
st.title("Home Page!")