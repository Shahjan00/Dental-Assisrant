import re


def mock_intent(query):
    q = query.lower()
    rtype = None
    for t in ["opg", "iopa", "cbct"]:
        if t in q:
            rtype = t.upper()
    stop = {"open", "show", "get", "latest", "report", "reports", "the",
            "a", "an", "my", "me", "please", "opg", "iopa", "cbct"}
    cleaned = re.sub(r"'s\b", "", query)
    words = re.findall(r"[A-Za-z]+", cleaned)
    name = " ".join(w for w in words if w.lower() not in stop).strip()
    return {"patient_name": name or None, "report_type": rtype}


def mock_dictation(transcript):
    teeth = re.findall(r"\((\d{2})\)", transcript)
    site = f"Tooth {teeth[0]}" if teeth else None
    low = any(w in transcript.lower() for w in ["maybe", "possible", "unclear"])
    return {
        "findings": [{
            "observation": transcript.strip(),
            "anatomical_site": site,
            "confidence": "low" if low else "medium",
            "requires_review": True,
        }],
        "uncertainty_notes": ["Hedging language found, verify clinically."] if low else [],
    }


def mock_followup(message, context):
    report = context.get("report", {})
    findings = report.get("findings", [])
    text = "; ".join(findings) if findings else "No findings recorded."
    return {
        "reply": f"Summary of {report.get('type', 'report')} ({report.get('date', '?')}): {text}",
        "evidence": findings,
    }
