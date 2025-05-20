import streamlit as st

MAX_INPUT_LENGTH = 1000

def validate_input(text: str) -> bool:
    if not text.strip():
        st.warning("Input cannot be empty.")
        return False
    if len(text) > MAX_INPUT_LENGTH:
        st.warning(f"Input too long ({len(text)} > {MAX_INPUT_LENGTH}).")
        return False
    return True
