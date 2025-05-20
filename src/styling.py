import streamlit as st

def apply_styling():
    st.markdown(
        """
        <style>
        .stButton>button {
            background: #FF8200;
            color: white;
            border-radius: 6px;
        }

        .stButton>button:hover {
            background: #e26e00;
        }

        input, textarea {
            border-radius: 6px !important;
            color: #F8FAFC !important;
        }

        div[data-testid="stChatMessage"] {
            background: #1E2230;
            border-radius: 8px;
            padding: .75rem 1rem !important;
            margin-bottom: .5rem;
            color: #F8FAFC;
        }

        div[data-testid="stChatMessage"]:has(svg[data-testid='icon-user']) {
            background: #2A2E3A;
        }

        div[data-testid="stChatMessage"]:has(svg[data-testid='icon-bot']) {
            background: #171B26;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
