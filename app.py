from dotenv import load_dotenv
load_dotenv()

import streamlit as st
st.set_page_config(layout="wide", page_title="Jinja Tourism Assistant — Sunbird AI", page_icon="🦜")


from src.config import SUPPORTED_LANGUAGES
from src.utils.chat import handle_chat_interaction


st.sidebar.image("img/sunbird-favicon.jpg", use_container_width=True)
st.sidebar.markdown("#### Sunbird AI — Tourism Demo")
st.sidebar.markdown(
    """
    <div style="display: flex; align-items: center;">
        <img src="https://sunbird.ai/favicon.ico" width="24" style="margin-right: 8px;">
        <span>This demo showcases Sunbird AI's multilingual capabilities.</span>
    </div>
    """,
    unsafe_allow_html=True,
)
ui_language = st.sidebar.selectbox("Choose language", list(SUPPORTED_LANGUAGES.keys()))

st.title("Enroute UG")
st.caption("From the hills to the city we speak your journey.")

handle_chat_interaction(ui_language)
