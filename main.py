from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from explanation_module import explain_concept
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# HTML templates
templates = Jinja2Templates(
    directory="templates"
)


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# ---------------------------------------------------------
# QUESTION ANSWERING
# Endpoint: /qa
# ---------------------------------------------------------

@app.post("/qa")
async def qa(payload: dict):

    question = payload.get("question", "").strip()

    if not question:
        return JSONResponse(
            content={
                "error": "Please enter a question."
            },
            status_code=400
        )

    answer = answer_question(question)

    return {
        "answer": answer
    }


# ---------------------------------------------------------
# CONCEPT EXPLANATION
# Endpoint: /explain
# ---------------------------------------------------------

@app.post("/explain")
async def explain(payload: dict):

    topic = payload.get("topic", "").strip()

    if not topic:
        return JSONResponse(
            content={
                "error": "Please enter a topic."
            },
            status_code=400
        )

    explanation = explain_concept(topic)

    return {
        "explanation": explanation
    }


# ---------------------------------------------------------
# QUIZ GENERATION
# Endpoint: /quiz
# ---------------------------------------------------------

@app.post("/quiz")
async def quiz(payload: dict):

    text = payload.get("text", "").strip()

    if not text:
        return JSONResponse(
            content={
                "error": "Please enter a topic or passage."
            },
            status_code=400
        )

    quiz_data = generate_quiz(text)

    return {
        "quiz": quiz_data
    }


# ---------------------------------------------------------
# SUMMARY
# Endpoint: /summarize
# ---------------------------------------------------------

@app.post("/summarize")
async def summarize(payload: dict):

    text = payload.get("text", "").strip()

    if not text:
        return JSONResponse(
            content={
                "error": "Please enter text to summarize."
            },
            status_code=400
        )

    summary = summarize_text(text)

    return {
        "summary": summary
    }


# ---------------------------------------------------------
# LEARNING PATH
# Endpoint: /learn/recommendations
# ---------------------------------------------------------

@app.post("/learn/recommendations")
async def recommendations(payload: dict):

    topic = payload.get("topic", "").strip()

    if not topic:
        return JSONResponse(
            content={
                "error": "Please enter a topic."
            },
            status_code=400
        )

    recommendations = get_learning_recommendations(topic)

    return {
        "recommendations": recommendations
    }