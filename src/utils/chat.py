import streamlit as st
from openai import OpenAI

from src.config import DEFAULT_MODEL, SUPPORTED_LANGUAGES, ASR_LANGUAGE_CODES
from src.utils.asr import transcribe_audio
from src.utils.common import validate_input
from src.utils.translate import ug40_translate, translate_texts
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def tourism_answer(question: str, lang: str) -> str:
    print(f"Answering question: {question} in language: {lang}")
    print(f"ASR language code: {ASR_LANGUAGE_CODES[lang]}")
    if lang == "English":
        # Use the default model for English
        messages = [
            {"role": "system", "content": "You are a friendly Jinja tour guide."},
            {"role": "user", "content": question},
        ]
        return call_openai(messages)
    else:
        # Use the translation model for other languages
        question = ug40_translate(question, "English")
        print(f"Translated question: {question}")
        messages = [
            {"role": "system", "content": "You are a friendly Jinja tour guide. Reply only in English."},
            {"role": "user", "content": question},
        ]
        
        response = call_openai(messages)
        response_texts = response.split("\n")
        translated_response = translate_texts(response_texts, ASR_LANGUAGE_CODES["English"], ASR_LANGUAGE_CODES[lang])
        print(f"Translated response: {translated_response}")
        return translated_response
    

def call_openai(messages, model=DEFAULT_MODEL):
    try:
        # Convert messages to a prompt string
        prompt_str = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt_str += "System: " + msg["content"] + "\n"
            elif msg["role"] == "user":
                prompt_str += "User: " + msg["content"] + "\n"
        prompt_str += "Assistant:"
        resp = client.responses.create(
            input=prompt_str,
            model=model,
        )
        print(f"OpenAI response: {resp.output_text}")
        return resp.output_text.strip()
    except Exception as exc:
        print(f"OpenAI error: {exc}")
        st.error(f"OpenAI error: {exc}")
        return "(Sorry, something went wrong.)"

def handle_chat_interaction(language: str):
    print(f"Handling chat interaction for language: {language}")
    lang_key = f"{language}_chat"
    st.session_state.chat_history = st.session_state.get("chat_history", {})
    st.session_state.chat_history.setdefault(lang_key, [])

    # 1. Display chat history
    for msg in st.session_state.chat_history[lang_key]:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        else:
            st.chat_message("assistant").markdown(msg["content"])

    # 2. Layout for input (audio + text) at the bottom
    col1, col2 = st.columns([1, 4])
    with col1:
        audio_bytes = st.audio_input("🎙️ Record your question", label_visibility="hidden", key="audio_input")
    with col2:
        prompt = st.chat_input(f"Type your question in {language}…")

    # --- Fix: Only process audio if not already processed ---
    if audio_bytes and not st.session_state.get("audio_processed", False):
        transcript = transcribe_audio(language, audio_bytes)
        if transcript and validate_input(transcript):
            st.session_state.chat_history[lang_key].append({"role": "user", "content": transcript})
            with st.spinner("Thinking…"):
                reply = tourism_answer(transcript, SUPPORTED_LANGUAGES[language])
            st.session_state.chat_history[lang_key].append({"role": "assistant", "content": reply})
            st.session_state.audio_processed = True  # Set flag
            st.rerun()  # Refresh to show new messages and reset recorder

    # --- Reset the flag when there's no audio_bytes (i.e., after rerun and widget is cleared) ---
    if not audio_bytes and st.session_state.get("audio_processed", False):
        st.session_state.audio_processed = False

    # 4. Handle text input
    if prompt and validate_input(prompt):
        st.session_state.chat_history[lang_key].append({"role": "user", "content": prompt})
        with st.spinner("Thinking…"):
            reply = tourism_answer(prompt, SUPPORTED_LANGUAGES[language])
        st.session_state.chat_history[lang_key].append({"role": "assistant", "content": reply})
        st.rerun()
