"""Deterministic rule-based provider. Used when no GEMINI_API_KEY is set."""
import re
from typing import Dict, Any
from app.llm.provider import LLMProvider


class MockProvider(LLMProvider):
    REPORT_TYPES = ["OPG", "IOPA", "CBCT"]

    def extract_retrieval_intent(self, query: str) -> Dict[str, Any]:
        q = query.lower()
        report_type = next(
            (t for t in self.REPORT_TYPES if t.lower() in q), None
        )
        # naive name extraction: capitalised words that aren't keywords
        stopwords = {"open", "show", "get", "latest", "report", "reports",
                     "the", "a", "an", "my", "me", "please", "opg", "iopa", "cbct"}
        # strip possessives first ("Priya's" -> "Priya")
        cleaned = re.sub(r"'s\b", "", query)
        words = re.findall(r"[A-Za-z]+", cleaned)
        name_parts = [w for w in words if w.lower() not in stopwords]
        patient_name = " ".join(name_parts).strip()
        return {"patient_name": patient_name or None, "report_type": report_type}

    def structure_dictation(self, transcript: str) -> Dict[str, Any]:
        # find FDI tooth numbers like (48), (26)
        teeth = re.findall(r"\((\d{2})\)", transcript)
        site = f"Tooth {teeth[0]}" if teeth else None
        low_conf = any(w in transcript.lower()
                       for w in ["maybe", "possible", "?", "unclear", "suspect"])
        return {
            "findings": [{
                "observation": transcript.strip(),
                "anatomical_site": site,
                "confidence": "low" if low_conf else "medium",
                "requires_review": True,
            }],
            "uncertainty_notes": (
                ["Hedging language detected; verify clinically."]
                if low_conf else []
            ),
        }

    def answer_followup(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        report = context.get("report") or {}
        findings = report.get("findings", [])
        summary = "; ".join(findings) if findings else "No findings recorded."
        return {
            "reply": f"Summary of {report.get('type', 'report')} "
                     f"({report.get('date', 'unknown date')}): {summary}",
            "evidence": findings,
        }
