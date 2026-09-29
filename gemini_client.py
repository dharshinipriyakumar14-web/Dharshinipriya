"""Shared Gemini helper used by every module."""
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to the .env file.")
        _client = genai.Client(api_key=api_key)
    return _client


def generate(prompt: str, json_mode: bool = False) -> str:
    config = types.GenerateContentConfig(response_mime_type="application/json") if json_mode else None
    response = _get_client().models.generate_content(
        model=MODEL_NAME, contents=prompt, config=config
    )
    text = (response.text or "").strip()
    if not text:
        raise ValueError("Gemini returned an empty response. Try rephrasing your input.")
    return text
