import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.models import RetrieveRequest, RetrieveResponse, DictateRequest, DictationResult, ChatRequest, ChatResponse
from app.services import retrieval, dictation, conversation
from app.llm.provider import get_llm

app = FastAPI(title="Dental Assistant")
llm = get_llm()

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def home():
    idx = os.path.join(static_dir, "index.html")
    if os.path.exists(idx):
        return FileResponse(idx)
    return {"message": "Dental Assistant API. See /docs for endpoints."}


@app.get("/health")
def health():
    return {"status": "ok", "llm": llm["name"]}


@app.post("/api/retrieve", response_model=RetrieveResponse)
def api_retrieve(req: RetrieveRequest):
    result = retrieval.retrieve_report(req.query, llm)
    sid = req.session_id or str(uuid.uuid4())
    if result["status"] == "found":
        conversation.save_context(sid, result["patient"], result["report"])
    return RetrieveResponse(session_id=sid, **result)


@app.post("/api/dictate", response_model=DictationResult)
def api_dictate(req: DictateRequest):
    if not req.transcript.strip():
        raise HTTPException(422, "transcript is empty")
    return DictationResult(**dictation.dictate(req.transcript, llm))


@app.post("/api/chat", response_model=ChatResponse)
def api_chat(req: ChatRequest):
    return ChatResponse(**conversation.chat(req.message, req.session_id, llm))
