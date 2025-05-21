from openai import OpenAI
import os
import requests
import backoff  # pip install backoff
import streamlit as st
from dotenv import load_dotenv, find_dotenv
import logging

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RUNPOD_API_KEY = os.getenv("SUNBIRD_RUNPOD_API_KEY", st.secrets["SUNBIRD_RUNPOD_API_KEY"])
RUNPOD_ENDPOINT_ID = os.getenv("SUNBIRD_RUNPOD_ENDPOINT_ID", st.secrets["SUNBIRD_RUNPOD_ENDPOINT_ID"])
MODEL_NAME = "patrickcmd/gemma3-12b-ug40-merged"

if not RUNPOD_API_KEY:
    raise ValueError("Missing SUNBIRD_RUNPOD_API_KEY in environment.")
if not RUNPOD_ENDPOINT_ID:
    raise ValueError("Missing SUNBIRD_RUNPOD_ENDPOINT_ID in environment.")

client = OpenAI(
    api_key=RUNPOD_API_KEY,
    base_url=f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/openai/v1",
)

@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
def ug40_translate(instruction: str, language: str) -> str:
    """
    Translates the given instruction into the specified language using a multilingual instruction-tuned model.

    Args:
        instruction (str): The text to be translated.
        language (str): The target language for translation (e.g., "English").

    Returns:
        str: The translated text.

    Raises:
        Exception: If the translation process fails.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a multilingual assistant specialising in Ugandan languages. You give accurate, precise translations."},
                {"role": "user", "content": f"Translate to {language}: {instruction}"},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error in translation: {e}")
        raise Exception("Translation failed.") from e


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
def translate(text, source_language, target_language):
    try:
        url = "https://api.sunbird.ai/tasks/nllb_translate"
        token = os.getenv("AUTH_TOKEN", st.secrets["AUTH_TOKEN"])
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        data = {
            "source_language": source_language,
            "target_language": target_language,
            "text": text,
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        # print(f"Response: {response.json()}")
        return response.json()["output"].get("translated_text")
    except Exception as e:
        logger.error(f"Error in translation: {e}")
        raise Exception("Translation failed.") from e

def translate_texts(texts: list, source_language: str = "eng", target_language: str = "lug") -> str:
    translated_texts = []
    for line in texts:
        line = line.strip()
        logger.info(f"Translating line: {line}")
        if not line:
            continue
        try:
            translated_texts.append(translate(line, source_language, target_language) + "\n")
        except Exception as e:
            return "**Error:** Some thing wrong happened! Please try again."
    final_text = "".join(translated_texts)
    return final_text

if __name__ == "__main__":
    # Example usage
    instruction = "Mbuulira awo ku byobulambuzi ebiri mu Fort Porto mu Uganda."
    translated_text = ug40_translate(instruction, "English")
    print(f"Translated text: {translated_text}")

    instruction = "We are going to an Arsenal game in London."
    translated_text = ug40_translate(instruction, "Luganda")
    print(f"Translated text: {translated_text}")

    text = open("src/utils/translate_text.txt", "r").readlines()
    # print(f"Text to translate: {text}")
    
    final_text = translate_texts(text, "eng", "lug")
    print(f"Translated text: {final_text}")
