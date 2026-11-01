import os
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI


class IntentOut(BaseModel):
    patient_name: Optional[str] = Field(None, description="patient name from the request")
    report_type: Optional[str] = Field(None, description="OPG, IOPA, CBCT or null")


class FindingOut(BaseModel):
    observation: str
    anatomical_site: Optional[str] = None
    confidence: str = "medium"
    requires_review: bool = True


class DictationOut(BaseModel):
    findings: List[FindingOut]
    uncertainty_notes: List[str] = []


class FollowupOut(BaseModel):
    reply: str
    evidence: List[str] = []


def _chat():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.environ["GEMINI_API_KEY"],
        temperature=0,
    )


def gemini_intent(query):
    llm = _chat().with_structured_output(IntentOut)
    out = llm.invoke(
        "Extract the patient name and report type (OPG/IOPA/CBCT) "
        f"from this dental report request:\n\n{query}"
    )
    return {"patient_name": out.patient_name, "report_type": out.report_type}


def gemini_dictation(transcript):
    llm = _chat().with_structured_output(DictationOut)
    out = llm.invoke(
        "Convert this dentist's spoken observation into structured findings. "
        "Do NOT invent anything not stated. Flag uncertainty.\n\n"
        f"{transcript}"
    )
    return {
        "findings": [f.model_dump() for f in out.findings],
        "uncertainty_notes": out.uncertainty_notes,
    }


def gemini_followup(message, context):
    import json
    llm = _chat().with_structured_output(FollowupOut)
    out = llm.invoke(
        "Answer using ONLY the report below. If the answer isn't there, say so.\n\n"
        f"Report: {json.dumps(context.get('report', {}))}\n"
        f"Question: {message}"
    )
    return {"reply": out.reply, "evidence": out.evidence}
