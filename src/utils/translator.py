import streamlit as st
from src.config import SUPPORTED_LANGUAGES
from src.utils.chat import call_openai
from src.utils.common import validate_input

def handle_translation_tab():
    src_text = st.text_area("Enter text to translate", height=120)
    col1, col2 = st.columns(2)
    with col1:
        tgt_lang = st.selectbox("Translate into …", list(SUPPORTED_LANGUAGES.keys()))
    with col2:
        do_translate = st.button("Translate")

    if do_translate and validate_input(src_text):
        messages = [
            {"role": "system", "content": f"You are a multilingual translator. Translate to {tgt_lang}."},
            {"role": "user", "content": src_text}
        ]
        with st.spinner("Translating…"):
            result = call_openai(messages)
            st.session_state.last_translation = result

    if st.session_state.get("last_translation"):
        st.text_area("Translation", st.session_state.last_translation, height=120)
