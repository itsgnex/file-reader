# ---------------------------------------------
# IMPORTANT: Disable HuggingFace tokenizer warnings
# This must be set BEFORE importing transformers
# ---------------------------------------------
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ---------------------------------------------
# Standard library imports
# ---------------------------------------------
import os

# ---------------------------------------------
# FastAPI imports
# ---------------------------------------------
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------
# Internal project imports
# ---------------------------------------------
from backend.transcribe import transcribe_audio
from backend.summarize import generate_summary
from backend.qa import answer_question

# ---------------------------------------------
# Create FastAPI application
# ---------------------------------------------
app = FastAPI()

# ---------------------------------------------
# Enable CORS so frontend can talk to backend
# (safe for local / demo usage)
# ---------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------
# Upload directory (created if missing)
# ---------------------------------------------
UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------------------------------------
# Allowed audio file extensions
# Backend NEVER trusts frontend alone
# ---------------------------------------------
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg"}

# ---------------------------------------------
# Store most recent processed text (v1 approach)
# This allows Q&A without a database
# ---------------------------------------------
latest_text = ""

# ---------------------------------------------
# POST /upload
# Handles:
# - File validation
# - Audio transcription
# - Translation
# - Summary generation
# ---------------------------------------------
@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    global latest_text

    # -----------------------------------------
    # Guard 1: No file provided
    # -----------------------------------------
    if not file or not file.filename:
        raise HTTPException(
            status_code=422,
            detail="No file uploaded"
        )

    # -----------------------------------------
    # Guard 2: File extension validation
    # -----------------------------------------
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    # -----------------------------------------
    # Save uploaded file to disk
    # -----------------------------------------
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # -----------------------------------------
    # Transcribe and translate audio (local)
    # -----------------------------------------
    original_text, translated_text = transcribe_audio(file_path)

    # -----------------------------------------
    # Guard 3: Transcription failed
    # -----------------------------------------
    if not translated_text.strip():
        raise HTTPException(
            status_code=500,
            detail="Transcription failed"
        )

    # -----------------------------------------
    # Generate summary from translated text
    # -----------------------------------------
    summary = generate_summary(translated_text)

    # -----------------------------------------
    # Save text for Q&A endpoint
    # -----------------------------------------
    latest_text = translated_text

    # -----------------------------------------
    # Return results to frontend
    # -----------------------------------------
    return {
        "transcription": original_text,
        "translation": translated_text,
        "summary": summary
    }

# ---------------------------------------------
# POST /ask
# Answers questions about the last uploaded file
# ---------------------------------------------
@app.post("/ask")
async def ask_question(question: str):
    # Guard: empty question
    if not question.strip():
        return {"answer": "Please enter a question."}

    return {
        "answer": answer_question(question, latest_text)
    }
