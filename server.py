"""RecallBuddy FastAPI server serving a custom HTML frontend."""

import os
import shutil
import tempfile
from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Import our existing backend
from ingestion.loader import load_text, load_pdf_text
from ingestion.chunker import split_into_chunks
from config import build_vectorstore
from quiz.generator import generate_question
from quiz.grader import grade_answer
from progress.tracker import ProgressTracker
from quiz.models import QuizQuestion

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Global state (for simplicity in a local app)
vectorstore = None
tracker = ProgressTracker()


class GenerateQuizRequest(BaseModel):
    topic: str


class GradeRequest(BaseModel):
    question: str
    options: list[str]
    correct_index: int
    user_index: int
    context: str


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/api/load_material")
def load_material():
    try:
        text = load_text("data/sample_article.txt")
        chunks = split_into_chunks(text)
        global vectorstore
        vectorstore = build_vectorstore(chunks)
        return {"status": "success", "message": "Material loaded"}
    except Exception as e:
        print(f"BACKEND ERROR: {repr(e)}")
        return {"status": "error", "message": str(e)}


@app.post("/api/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process a PDF file, building the vectorstore from its content."""
    if not file.filename.endswith(".pdf"):
        return {"status": "error", "message": "Only PDF files are supported."}

    temp_path = None
    try:
        # Save uploaded file temporarily
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, file.filename)
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Extract text and build vectorstore
        text = load_pdf_text(temp_path)
        chunks = split_into_chunks(text)
        global vectorstore
        vectorstore = build_vectorstore(chunks)

        return {"status": "success", "message": "PDF loaded successfully."}
    except Exception as e:
        print(f"BACKEND ERROR: {repr(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            try:
                os.rmdir(os.path.dirname(temp_path))
            except OSError:
                pass


@app.post("/api/generate_question")
def api_generate_question(req: GenerateQuizRequest):
    try:
        if vectorstore is None:
            raise HTTPException(status_code=400, detail="Material not loaded. Call /api/load_material first.")
        quiz_q = generate_question(vectorstore, req.topic)
        return {
            "question": quiz_q.question,
            "options": quiz_q.options,
            "correct_index": quiz_q.correct_index,
            "explanation": quiz_q.explanation,
            "source_chunk": quiz_q.source_chunk,
        }
    except Exception as e:
        print(f"BACKEND ERROR: {repr(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate question: {str(e)}")


@app.post("/api/grade_answer")
def api_grade_answer(req: GradeRequest):
    try:
        quiz_q = QuizQuestion(
            question=req.question,
            options=req.options,
            correct_index=req.correct_index,
            explanation="",
            source_chunk=req.context,
        )
        explanation = grade_answer(quiz_q, req.user_index)
        is_correct = req.user_index == req.correct_index
        tracker.record_attempt(req.question, req.question, is_correct)
        return {
            "is_correct": is_correct,
            "explanation": explanation,
            "stats": tracker.get_stats(),
        }
    except Exception as e:
        print(f"BACKEND ERROR: {repr(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to grade answer: {str(e)}")