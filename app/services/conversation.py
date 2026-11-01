"""Feature C: conversational follow-up with session memory."""
from typing import Dict, Any, Optional
from app.llm.provider import LLMProvider

_sessions: Dict[str, Dict[str, Any]] = {}


def set_context(session_id: str, patient: Dict[str, Any],
                report: Dict[str, Any]) -> None:
    _sessions[session_id] = {"patient": patient, "report": report}


def get_context(session_id: str) -> Optional[Dict[str, Any]]:
    return _sessions.get(session_id)


def followup(message: str, session_id: str, llm: LLMProvider) -> Dict[str, Any]:
    ctx = _sessions.get(session_id)
    if not ctx or not ctx.get("report"):
        return {
            "reply": "I don't have a report in context yet. "
                     "Retrieve one first, e.g. \"Open Priya Sharma's latest OPG report\".",
            "evidence": [],
            "session_id": session_id,
        }
    result = llm.answer_followup(message, ctx)
    return {
        "reply": result.get("reply", ""),
        "evidence": result.get("evidence", []),
        "session_id": session_id,
    }
