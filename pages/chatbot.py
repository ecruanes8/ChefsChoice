import streamlit as st 
import streamlit_authenticator as stauth
import yaml 
from yaml.loader import SafeLoader 
from langchain_openai.chat_models import ChatOpenAI

# re-load login 
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
st.title("Chatbot!")

open_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

def generate_response(input_text): 
    model = ChatOpenAI(temperature=0.7, api_key=open_api_key)
    st.info(model.invoke(input_text))