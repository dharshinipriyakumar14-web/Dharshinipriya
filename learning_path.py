"""Personalized learning path with Gemini."""
from gemini_client import generate


def get_learning_recommendations(topic: str) -> str:
    prompt = (
        f"Create a structured learning path for: {topic}\n\n"
        "Organize it into three levels: Beginner, Intermediate, Advanced. For each level give:\n"
        "- Key concepts to learn, in order\n"
        "- An estimated timeline\n"
        "- Recommended resources (videos, articles, books, practice sites)\n"
        "- One small practice project\n"
        "Finish with 3 short study tips. Use Markdown headings and bullet points."
    )
    return generate(prompt)
