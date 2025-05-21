"""
Streamlit App: Jinja Tourism Multilingual Assistant
Designed by Sunbird AI — © 2025
===================================================
A polished, audio‑enabled Streamlit app that answers tourism questions about
**Jinja, Uganda** in **English, Runyankole, or Luganda** and offers an instant
translator. Users can type **or record audio**; Sunbird ASR converts speech to
text and the chat replies in the same language.
"""

from __future__ import annotations
import os
from typing import Dict, List

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),
api_key=os.getenv("OPENAI_API_KEY"))
from openai import OpenAI
import requests
import streamlit as st
from st_audiorec import st_audiorec
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────────────────────────────────────
# 🔧 CONFIGURATION & CONSTANTS
# ──────────────────────────────────────────────────────────────────────────────
if not openai.api_key:
    st.error("OPENAI_API_KEY environment variable not set. Please set it for the app to function.")
SUNBIRD_ASR_URL = os.getenv("SUNBIRD_ASR_URL", "https://api.sunbird.ai/speech-to-text")
client = OpenAI()

SUPPORTED_LANGUAGES: Dict[str, str] = {
    "English": "English",
    "Runyankole": "Runyankole",
    "Luganda": "Luganda",
}
DEFAULT_MODEL = "gpt-4o-mini"

# Sunbird palette (WCAG‑friendly)
SUNBIRD_PRIMARY   = "#FF8200"  # vivid orange
SUNBIRD_SECONDARY = "#004C99"  # deep blue
SUNBIRD_CANVAS    = "#F7FAFC"  # page background
SUNBIRD_CARD      = "#FFFFFF"  # surfaces / cards
SUNBIRD_BORDER    = "#CED9E5"  # soft border
USER_BUBBLE_BG    = "#FFF4EB"  # 10 % orange
BOT_BUBBLE_BG     = "#EAF2FF"  # 10 % blue

st.set_page_config(
    page_title="Jinja Tourism Assistant — Sunbird AI",
    page_icon="🦜",
    layout="centered",
)

# ──────────────────────────────────────────────────────────────────────────────
# 🎨 GLOBAL STYLING
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <style>
        :root {{
            --sb-primary:   {SUNBIRD_PRIMARY};
            --sb-secondary: {SUNBIRD_SECONDARY};
            --sb-canvas:    {SUNBIRD_CANVAS};
            --sb-card:      {SUNBIRD_CARD};
            --sb-border:    {SUNBIRD_BORDER};
            --sb-user-bg:   {USER_BUBBLE_BG};
            --sb-bot-bg:    {BOT_BUBBLE_BG};
        }}

        /* Base canvas */
        .stApp {{ background: var(--sb-canvas); font-family: "Segoe UI", Roboto, sans-serif; }}
        .block-container {{ padding-top: 1.5rem; }}

        /* Headings */
        h1,h2,h3,h4,h5,h6 {{ color: var(--sb-secondary); margin-bottom:.25rem; }}

        /* Sidebar spacing */
        section[data-testid="stSidebar"] > div:first-child {{ padding-top:1rem; }}
        section[data-testid="stSidebar"] img {{ margin-bottom:1.2rem; }}

        /* Buttons */
        .stButton>button {{ background:var(--sb-primary); color:#FFF; border:none; border-radius:6px; padding:.5rem 1.4rem; transition:background .15s; }}
        .stButton>button:hover {{ background:#e26e00; }}

        /* Inputs */
        input, textarea {{ border:1px solid var(--sb-border)!important; border-radius:6px!important; background:var(--sb-card)!important; color:#1F2933!important; }}
        input::placeholder, textarea::placeholder {{ color:#64748B; }}

        /* Chat bubbles */
        div[data-testid="stChatMessage"] {{ background:var(--sb-card); border:1px solid var(--sb-border); border-radius:8px; padding:.75rem 1rem!important; margin-bottom:.5rem; }}
        div[data-testid="stChatMessage"]:has(svg[data-testid='icon-user']) {{ background:var(--sb-user-bg); }}
        div[data-testid="stChatMessage"]:has(svg[data-testid='icon-bot'])  {{ background:var(--sb-bot-bg);  }}

        /* Tabs underline */
        div[data-baseweb="tab-bar"] > div {{ border-bottom:3px solid var(--sb-primary); }}
        button[role="tab"] {{ color:var(--sb-secondary); font-weight:500; }}
        button[aria-selected="true"][role="tab"] {{ color:var(--sb-primary); }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# 🧠 HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────

MAX_INPUT_LENGTH = 1000

def validate_input(text: str) -> bool:
    if not text.strip():
        st.warning("Input cannot be empty.")
        return False
    if len(text) > MAX_INPUT_LENGTH:
        st.warning(f"Input too long (>{MAX_INPUT_LENGTH} characters). Please shorten your message.")
        return False
    return True


def call_openai(messages: List[Dict[str, str]], model: str = DEFAULT_MODEL) -> str:
    """Wrapper around OpenAI Chat Completion."""
    try:
        resp = client.responses.create(model=model, input=messages)
        return resp.output_text
    except Exception as exc:
        st.error(f"OpenAI error: {exc}")
        return "(Sorry, something went wrong.)"


def translate(text: str, target_lang: str) -> str:
    sys_prompt = (
        "You are a professional translator fluent in English, Runyankole, and Luganda. "
        f"Translate the user's text into {target_lang}. Preserve meaning and tone."
    )
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": text},
    ]
    return call_openai(messages)


def tourism_answer(question: str, lang: str) -> str:
    sys_prompt = (
        "You are a friendly, concise, factual tour guide for Jinja, Uganda. "
        "Your knowledge covers attractions (Source of the Nile, Itanda & Bujagali Falls, kayaking, etc.), history, culture, transport, and indicative prices up to May 2025. "
        "Respond ONLY in {lang}."
    ).format(lang=lang)
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": question},
    ]
    return call_openai(messages)


def transcribe_audio_from_sunbird(audio_bytes: bytes, language_hint: str) -> str:
    """Send WAV bytes to Sunbird ASR and return the transcript."""
    try:
        headers = {"Content-Type": "audio/wav"}
        params = {"language": language_hint.lower()}
        resp = requests.post(SUNBIRD_ASR_URL, headers=headers, params=params, data=audio_bytes, timeout=60)
        resp.raise_for_status()
        try:
            return resp.json().get("text", "")
        except ValueError:
            st.error("ASR response was not valid JSON.")
            return ""
    except Exception as exc:
        st.error(f"ASR error: {exc}")
        return ""

# ──────────────────────────────────────────────────────────────────────────────
# 🎨 SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://raw.githubusercontent.com/sunbirdai/assets/main/logo/sunbird_logo.png",
        use_container_width=True,
    )
    st.markdown("#### Sunbird AI — Tourism Demo")
    st.info("This demo showcases Sunbird AI's multilingual capabilities using the OpenAI API.", icon="ℹ️")
    ui_language = st.selectbox(
        "Interface language / Olu'nyonjo lw'okozesa / Enyikyo ey'okukozesa",
        list(SUPPORTED_LANGUAGES.keys())
    )

# Initialize chat history per language
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

# ──────────────────────────────────────────────────────────────────────────────
# 🚀 MAIN LAYOUT
# ──────────────────────────────────────────────────────────────────────────────
st.title("🏞️ Jinja Tourism Assistant")
st.caption("Ask anything about visiting Jinja — in English, Runyankole, or Luganda.")

chat_tab, translate_tab = st.tabs(["🗣️ Chat", "🔄 Translate"])

# ─── CHAT TAB ────────────────────────────────────────────────────────────────
with chat_tab:
    st.subheader("Ask your question")

    # ▶️ Record audio (optional)
    st.markdown("###### Or record your question:")
    audio_bytes = st_audiorec(
        text="Click to record", icon_size="2x", recording_color=SUNBIRD_PRIMARY, neutral_color="#4B5563"
    )

    lang_key = f"{ui_language}_chat"
    st.session_state.chat_history.setdefault(lang_key, [])

    # Handle audio → transcript → reply
    if audio_bytes:
        with st.spinner("Transcribing…"):
            user_text = transcribe_audio_from_sunbird(audio_bytes, SUPPORTED_LANGUAGES[ui_language])
        if user_text and validate_input(user_text):
            st.session_state.chat_history[lang_key].append({"role": "user", "content": user_text})
            st.chat_message("user").markdown(user_text)
            with st.spinner("Thinking…"):
                bot_reply = tourism_answer(user_text, SUPPORTED_LANGUAGES[ui_language])
            st.session_state.chat_history[lang_key].append({"role": "assistant", "content": bot_reply})
            st.chat_message("assistant").markdown(bot_reply)

    # Display previous messages
    for msg in st.session_state.chat_history[lang_key]:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # Text input fallback
    if prompt := st.chat_input(f"Type your question in {ui_language}…"):
        if validate_input(prompt):
            st.session_state.chat_history[lang_key].append({"role": "user", "content": prompt})
            st.chat_message("user").markdown(prompt)
            with st.spinner("Thinking…"):
                bot_reply = tourism_answer(prompt, SUPPORTED_LANGUAGES[ui_language])
            st.session_state.chat_history[lang_key].append({"role": "assistant", "content": bot_reply})
            st.chat_message("assistant").markdown(bot_reply)

# ─── TRANSLATE TAB ────────────────────────────────────────────────────────────
with translate_tab:
    st.subheader("Quick translator")
    src_text = st.text_area("Enter text to translate", height=120)
    col1, col2 = st.columns(2)
    with col1:
        tgt_lang = st.selectbox("Translate into …", list(SUPPORTED_LANGUAGES.keys()), index=0)
    with col2:
        translate_btn = st.button("Translate", use_container_width=True)

    if translate_btn and src_text:
        if validate_input(src_text):
            with st.spinner("Translating…"):
                tgt_text = translate(src_text, SUPPORTED_LANGUAGES[tgt_lang])
            st.success("Translation complete!")
            st.text_area("Translation", tgt_text, height=120)

# ──────────────────────────────────────────────────────────────────────────────
# 📢 FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("<hr style='border-top: 1px solid #EEE;'>", unsafe_allow_html=True)
st.markdown("<small>Built by <b>Sunbird AI</b> • MIT License • © 2025</small>", unsafe_allow_html=True)

###############################################################################
# Note: This code is a simplified version of the original app.py and utils.


import streamlit as st
import requests
import os
from dotenv import load_dotenv
from src.config import ASR_LANGUAGE_CODES

load_dotenv()

SUNBIRD_ASR_URL = "https://api.sunbird.ai/tasks/stt"
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

def transcribe_audio(language: str, audio_bytes: bytes) -> str:
    if not audio_bytes:
        return ""

    lang_code = ASR_LANGUAGE_CODES.get(language, "eng")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}",
    }

    files = {
        "audio": ("input.wav", audio_bytes, "audio/wav"),
    }

    data = {
        "language": lang_code,
        "adapter": lang_code,
        "whisper": "true",
    }

    try:
        with st.spinner("Transcribing via Sunbird…"):
            response = requests.post(
                SUNBIRD_ASR_URL,
                headers=headers,
                files=files,
                data=data,
                timeout=60
            )
            response.raise_for_status()
            return response.json().get("audio_transcription", "")
    except Exception as e:
        st.error(f"Sunbird ASR error: {e}")
        return ""


# This code is a simplified version of the original app.py and utils.

import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),
api_key=os.getenv("OPENAI_API_KEY"))
from src.config import DEFAULT_MODEL, SUPPORTED_LANGUAGES
from src.utils.asr import transcribe_audio
from src.utils.common import validate_input
import streamlit as st
import os


def tourism_answer(question: str, lang: str) -> str:
    messages = [
        {"role": "system", "content": f"You are a friendly Jinja tour guide. Reply only in {lang}."},
        {"role": "user", "content": question},
    ]
    return call_openai(messages)

def call_openai(messages, model=DEFAULT_MODEL):
    try:
        resp = client.chat.completions.create(model=model, messages=messages)
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        st.error(f"OpenAI error: {exc}")
        return "(Sorry, something went wrong.)"

def handle_chat_interaction(language: str):
    lang_key = f"{language}_chat"
    st.session_state.chat_history = st.session_state.get("chat_history", {})
    st.session_state.chat_history.setdefault(lang_key, [])

    # 1. Display chat history (WhatsApp style: user right, assistant left)
    for msg in st.session_state.chat_history[lang_key]:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        else:
            st.chat_message("assistant").markdown(msg["content"])

    # 2. Layout for input (audio + text) at the bottom
    col1, col2 = st.columns([1, 4])
    with col1:
        audio_bytes = st.audio_input("🎙️ Record your question",label_visibility="hidden")
        # st.audio(audio_bytes)
    with col2:
        prompt = st.chat_input(f"Type your question in {language}…")

    # 3. Handle audio input
    if audio_bytes:
        transcript = transcribe_audio(language, audio_bytes)
        if transcript and validate_input(transcript):
            st.session_state.chat_history[lang_key].append({"role": "user", "content": transcript})
            with st.spinner("Thinking…"):
                reply = tourism_answer(transcript, SUPPORTED_LANGUAGES[language])
            st.session_state.chat_history[lang_key].append({"role": "assistant", "content": reply})
            # st.experimental_rerun()  # Refresh to show new messages and reset recorder

    # 4. Handle text input
    if prompt and validate_input(prompt):
        st.session_state.chat_history[lang_key].append({"role": "user", "content": prompt})
        with st.spinner("Thinking…"):
            reply = tourism_answer(prompt, SUPPORTED_LANGUAGES[language])
        st.session_state.chat_history[lang_key].append({"role": "assistant", "content": reply})
        # st.experimental_rerun()  # Refresh to show new messages
