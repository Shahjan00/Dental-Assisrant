from app.llm.provider import safe_call

sessions = {}


def save_context(sid, patient, report):
    sessions[sid] = {"patient": patient, "report": report}


def chat(message, sid, llm):
    ctx = sessions.get(sid)
    if not ctx or not ctx.get("report"):
        return {"reply": "No report loaded yet. Try \"Open Priya Sharma's latest OPG report\" first.",
                "evidence": [], "session_id": sid, "fallback_used": False}
    out, used_fallback = safe_call(llm, "followup", message, ctx)
    return {"reply": out.get("reply", ""),
            "evidence": out.get("evidence", []),
            "session_id": sid,
            "fallback_used": used_fallback}
