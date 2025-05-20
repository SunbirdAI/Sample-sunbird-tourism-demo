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