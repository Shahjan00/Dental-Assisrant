"""Feature B: clinical dictation -> structured draft report. Never invents findings."""
from typing import Dict, Any
from app.llm.provider import LLMProvider


def dictate(transcript: str, llm: LLMProvider) -> Dict[str, Any]:
    text = (transcript or "").strip()
    if not text:
        return {
            "transcript": "",
            "findings": [],
            "draft_report": "",
            "uncertainty_notes": ["Empty transcript; nothing to document."],
            "clinician_review_required": True,
        }

    structured = llm.structure_dictation(text)
    findings = structured.get("findings", [])

    lines = ["DRAFT CLINICAL REPORT (requires clinician review)", ""]
    for i, f in enumerate(findings, 1):
        site = f.get("anatomical_site") or "site not specified"
        lines.append(f"{i}. [{site}] {f.get('observation','')}")
        lines.append(f"   Confidence: {f.get('confidence','medium')}")
    draft = "\n".join(lines)

    return {
        "transcript": text,
        "findings": findings,
        "draft_report": draft,
        "uncertainty_notes": structured.get("uncertainty_notes", []),
        "clinician_review_required": True,
    }
