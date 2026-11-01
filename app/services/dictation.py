from app.llm.provider import safe_call


def dictate(transcript, llm):
    text = (transcript or "").strip()
    if not text:
        return {"transcript": "", "findings": [], "draft_report": "",
                "uncertainty_notes": ["Empty transcript."],
                "clinician_review_required": True, "fallback_used": False}

    out, used_fallback = safe_call(llm, "dictation", text)

    lines = ["DRAFT REPORT (needs clinician review)", ""]
    for i, f in enumerate(out.get("findings", []), 1):
        site = f.get("anatomical_site") or "site unknown"
        lines.append(f"{i}. [{site}] {f.get('observation', '')}")

    return {"transcript": text,
            "findings": out.get("findings", []),
            "draft_report": "\n".join(lines),
            "uncertainty_notes": out.get("uncertainty_notes", []),
            "clinician_review_required": True,
            "fallback_used": used_fallback}
