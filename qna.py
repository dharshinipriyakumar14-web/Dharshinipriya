"""Question answering with Gemini."""
from gemini_client import generate


def answer_question(question: str) -> str:
    prompt = (
        "You are EduGenie, a friendly tutor. Answer the student's question accurately "
        "and concisely (under 150 words). Use simple language.\n\n"
        f"Question: {question}"
    )
    return generate(prompt)
