"""Pydantic schemas for the dental assistant."""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


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
    type: Literal["OPG", "IOPA", "CBCT"]
    date: str
    dentist: str
    findings: List[str]
    impression: str
    status: Literal["final", "draft"] = "final"


class Finding(BaseModel):
    observation: str
    anatomical_site: Optional[str] = None
    confidence: Literal["high", "medium", "low"] = "medium"
    requires_review: bool = True


class DictationResult(BaseModel):
    transcript: str
    findings: List[Finding]
    draft_report: str
    uncertainty_notes: List[str] = Field(default_factory=list)
    clinician_review_required: bool = True


class RetrieveRequest(BaseModel):
    query: str = Field(..., description='e.g. "Open Priya\'s latest OPG report"')
    session_id: Optional[str] = None


class RetrieveResponse(BaseModel):
    session_id: str = ""
    status: Literal["found", "ambiguous", "not_found"]
    patient: Optional[Patient] = None
    candidates: List[Patient] = Field(default_factory=list)
    report: Optional[Report] = None
    message: str
    evidence: List[str] = Field(default_factory=list)


class DictateRequest(BaseModel):
    transcript: str = Field(..., description="Speech-to-text transcript of clinical observation")
    session_id: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    session_id: str = Field(..., description="Session ID to maintain conversational context")


class ChatResponse(BaseModel):
    reply: str
    evidence: List[str] = Field(default_factory=list)
    session_id: str
