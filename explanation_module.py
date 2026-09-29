"""Concept explanation with the local LaMini-Flan-T5 model (falls back to Gemini)."""
from functools import lru_cache

from gemini_client import generate

MODEL_ID = "MBZUAI/LaMini-Flan-T5-783M"


@lru_cache(maxsize=1)
def _load_model():
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
    model.eval()
    return tokenizer, model


def _run_local(prompt: str) -> str:
    import torch

    tokenizer, model = _load_model()
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        output_ids = model.generate(
            **inputs, max_new_tokens=256, num_beams=2,
            no_repeat_ngram_size=3, early_stopping=True,
        )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()


def explain_concept(concept: str) -> str:
    prompt = f"Explain the following concept in simple words for a beginner:\n{concept}"
    try:
        text = _run_local(prompt)
        if text:
            return text
    except Exception as exc:  # model missing, no torch, out of memory, etc.
        print(f"[EduGenie] Local model unavailable ({exc}). Using Gemini instead.")
    return generate(prompt)
