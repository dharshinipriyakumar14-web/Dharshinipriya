"""Quiz generation: 3 multiple-choice questions with 4 options each."""
import json
import re

from gemini_client import generate

LETTERS = "ABCD"


def clean_json_block(text: str) -> str:
    """Strip Markdown code fences such as ```json ... ``` around a JSON reply."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_quiz(source: str) -> list:
    prompt = (
        "Create exactly 3 multiple-choice questions from the topic or passage below. "
        "Each question needs exactly 4 plausible options and one correct answer.\n"
        "Return ONLY a JSON array, no Markdown, in this format:\n"
        '[{"question": "...", "options": ["...", "...", "...", "..."], "correct_option": "A"}]\n'
        "Do not put letters like 'A)' inside the options. 'correct_option' is the letter "
        "(A, B, C or D) matching the position of the right option.\n\n"
        f"Topic or passage:\n{source}"
    )
    raw = generate(prompt, json_mode=True)
    try:
        data = json.loads(clean_json_block(raw))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not parse quiz JSON ({exc}). Raw reply: {raw[:300]}")

    if isinstance(data, dict):
        data = data.get("questions", [])

    quiz = []
    for item in data[:3]:
        options = [str(o) for o in item.get("options", [])][:4]
        letter = str(item.get("correct_option", "")).strip().upper()[:1]
        if len(options) != 4 or letter not in LETTERS:
            raise ValueError(f"Quiz question was malformed: {item}")
        quiz.append({
            "question": str(item.get("question", "")).strip(),
            "options": options,
            "answer_index": LETTERS.index(letter),
        })
    if not quiz:
        raise ValueError("No quiz questions were returned. Try again with more detail.")
    return quiz
