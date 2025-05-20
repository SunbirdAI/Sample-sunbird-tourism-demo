import os
import streamlit as st

# ENV VARS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUNBIRD_ASR_URL = os.getenv("SUNBIRD_ASR_URL")

if not OPENAI_API_KEY:
    st.error("Missing OPENAI_API_KEY in environment.")
    st.stop()

if not SUNBIRD_ASR_URL:
    st.error("Missing SUNBIRD_ASR_URL in environment.")
    st.stop()

SUPPORTED_LANGUAGES = {
    "English": "English",
    "Runyankole": "Runyankole",
    "Luganda": "Luganda",
}

ASR_LANGUAGE_CODES = {
    "English": "eng",
    "Runyankole": "nyn",
    "Luganda": "lug",
}

DEFAULT_MODEL = "gpt-4o-mini"
