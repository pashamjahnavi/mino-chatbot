import streamlit as st
from views import home, login, chatbot

# Page config
st.set_page_config(
    page_title="Mino",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto"
)

# Hide default menu and footer
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stSidebarNav"] {display: none !important;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# Page routing
if st.session_state.page == "home":
    home.show()
elif st.session_state.page == "login":
    login.show()
elif st.session_state.page == "chatbot":
    chatbot.show() 