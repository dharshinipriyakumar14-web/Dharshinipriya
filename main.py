"""EduGenie - FastAPI app. Run with: uvicorn main:app --reload"""
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="EduGenie")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class TextRequest(BaseModel):
    text: str


def run(handler, payload: TextRequest):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Please enter some text first.")
    try:
        return {"result": handler(text)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/qa")
def qa(payload: TextRequest):
    return run(answer_question, payload)


@app.post("/explain")
def explain(payload: TextRequest):
    return run(explain_concept, payload)


@app.post("/quiz")
def quiz(payload: TextRequest):
    return run(generate_quiz, payload)


@app.post("/summarize")
def summarize(payload: TextRequest):
    return run(summarize_text, payload)


@app.post("/learn/recommendations")
def recommendations(payload: TextRequest):
    return run(get_learning_recommendations, payload)
