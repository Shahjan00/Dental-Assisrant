"""FastAPI app: voice-first dental assistant (VI-SCAN take-home)."""
import uuid
from fastapi import FastAPI, HTTPException
from app.models import (
    RetrieveRequest, RetrieveResponse,
    DictateRequest, DictationResult,
    ChatRequest, ChatResponse,
)
from app.services import retrieval, dictation, conversation
from app.llm.gemini_provider import get_provider

app = FastAPI(title="Dental Assistant", version="0.1.0")
llm = get_provider()


@app.get("/health")
def health():
    return {"status": "ok", "llm": type(llm).__name__}


@app.post("/api/retrieve", response_model=RetrieveResponse)
def api_retrieve(req: RetrieveRequest):
    result = retrieval.retrieve_report(req.query, llm)
    session_id = req.session_id or str(uuid.uuid4())
    if result["status"] == "found":
        conversation.set_context(
            session_id, result["patient"], result["report"])
    return RetrieveResponse(session_id=session_id, **result)


@app.post("/api/dictate", response_model=DictationResult)
def api_dictate(req: DictateRequest):
    if not req.transcript or not req.transcript.strip():
        raise HTTPException(status_code=422, detail="transcript must not be empty")
    return DictationResult(**dictation.dictate(req.transcript, llm))


@app.post("/api/chat", response_model=ChatResponse)
def api_chat(req: ChatRequest):
    return ChatResponse(**conversation.followup(req.message, req.session_id, llm))
