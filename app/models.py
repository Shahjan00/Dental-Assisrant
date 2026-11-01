from pydantic import BaseModel
from typing import List, Optional


class Patient(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    phone: str
    email: str


class Report(BaseModel):
    id: str
    patient_id: str
    type: str
    date: str
    dentist: str
    findings: List[str]
    impression: str
    status: str = "final"


class RetrieveRequest(BaseModel):
    query: str
    session_id: Optional[str] = None


class RetrieveResponse(BaseModel):
    session_id: str = ""
    status: str
    patient: Optional[Patient] = None
    candidates: List[Patient] = []
    report: Optional[Report] = None
    message: str
    evidence: List[str] = []


class DictateRequest(BaseModel):
    transcript: str
    session_id: Optional[str] = None


class Finding(BaseModel):
    observation: str
    anatomical_site: Optional[str] = None
    confidence: str = "medium"
    requires_review: bool = True


class DictationResult(BaseModel):
    transcript: str
    findings: List[Finding]
    draft_report: str
    uncertainty_notes: List[str] = []
    clinician_review_required: bool = True


class ChatRequest(BaseModel):
    message: str
    session_id: str


class ChatResponse(BaseModel):
    reply: str
    evidence: List[str] = []
    session_id: str
