# Jinja Tourism Multilingual Assistant

**A Streamlit app for exploring Jinja, Uganda in English, Runyankole, or Luganda.**  
Designed by **Sunbird AI**, powered by **OpenAI ChatGPT** and **Sunbird ASR**.

---

## Features

|                                | Details                                                                                                                         |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| **Multilingual Chat**          | Ask tourism‑related questions in your chosen language (English, Runyankole, Luganda) and receive answers in that same language. |
| **Audio & Text Input**         | Type or record your question; audio is transcribed using Sunbird ASR.                                                           |
| **On‑the‑Fly Translation**     | Quick translator between any pair of the three supported languages.                                                             |
| **Sunbird‑Branded UI**         | Clean orange + deep‑blue palette, mobile‑friendly layout, logo in sidebar.                                                      |
| **Session‑based Chat History** | Conversations persist per language while the app is running.                                                                    |
| **OpenAI API Integration**     | Uses the Chat Completion endpoint for both Q\&A and translation.                                                                |
| **Custom Styling**             | WhatsApp-like chat bubbles and modern dark/light theme.                                                                         |

---

## Quick Start

```bash
# 1) Clone or download the repo
git clone https://github.com/your‑org/jinja‑tourism‑assistant.git
cd jinja‑tourism‑assistant

# 2) Create a virtual environment (recommended)
python -m venv .venv && source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Add your API keys (replace with your actual keys)
export OPENAI_API_KEY="sk-..."
export SUNBIRD_ASR_URL="https://api.sunbird.ai/speech-to-text"
export AUTH_TOKEN="..."

# Or use a .env file (see below)

# 5) Run the app
streamlit run app.py
```

> **Tip:**  
> If you prefer using a `.env`, install `python-dotenv` and create a file named `.env` with:
> ```
> OPENAI_API_KEY=sk-...
> SUNBIRD_ASR_URL=https://api.sunbird.ai/speech-to-text
> AUTH_TOKEN=...
> ```

---

## Project Structure

```text
.
├── app.py                       # Main Streamlit entrypoint (recommended)
├── jinja_tourism_app.py         # Legacy/standalone Streamlit app (optional)
├── requirements.txt             # Python dependencies
├── .env                         # (optional) API keys and config
├── .streamlit/
│   └── config.toml              # Theme and Streamlit config
├── src/
│   ├── config.py                # App configuration and constants
│   ├── styling.py               # Custom CSS/styling
│   └── utils/
│       ├── asr.py               # Sunbird ASR integration
│       ├── chat.py              # Chat logic and OpenAI integration
│       ├── common.py            # Input validation and helpers
│       └── translator.py        # Translation tab logic
└── README.md                    # You are here 📄
```

---

## Configuration

| Variable           | Purpose                                         | Required |
| ------------------ | ----------------------------------------------- | -------- |
| `OPENAI_API_KEY`   | Your OpenAI API key                             | **Yes**  |
| `SUNBIRD_ASR_URL`  | Sunbird ASR endpoint URL                        | **Yes**  |
| `AUTH_TOKEN`       | Sunbird ASR authentication token                | **Yes**  |

Set these as environment variables or in a `.env` file.

---

## Usage

- **Sidebar:** Choose your language and see Sunbird AI branding.
- **Chat Tab:** Type or record your question. Audio is transcribed and answered in your chosen language.
- **Translate Tab:** Instantly translate text between English, Runyankole, and Luganda.
- **Chat History:** Each language keeps its own session-based chat history.
- **Styling:** Modern, accessible, and mobile-friendly UI.

---

## Customization

- **Colour Palette:**  
  Defined in `src/styling.py` and at the top of `jinja_tourism_app.py`.
- **Model Choice:**  
  Change `DEFAULT_MODEL` in `src/config.py` (e.g., `gpt-4o-mini`).
- **Prompt Engineering:**  
  Tweak the system prompts in `src/utils/chat.py` for tone/content.
- **Add More Languages:**  
  Update `SUPPORTED_LANGUAGES` and `ASR_LANGUAGE_CODES` in `src/config.py`.

---

## Troubleshooting

- **Missing API Keys:**  
  The app will show an error if required keys are missing.
- **Audio Not Working:**  
  Ensure your browser supports audio recording and you have microphone permissions enabled.
- **Duplicate Messages:**  
  The app uses session state flags to prevent repeated processing of the same audio.

---

## Contributing

1. Fork the repo & create a feature branch.
2. Make your changes and add unit or manual tests where useful.
3. Open a PR describing the improvement or bug fix.

---

## License

```
MIT License © 2025 Sunbird AI