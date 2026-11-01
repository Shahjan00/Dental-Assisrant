"""Feature A: patient report retrieval. LLM extracts intent; tools enforce rules."""
from typing import Dict, Any
from app.llm.provider import LLMProvider
from app.tools import clinical_tools as tools


def retrieve_report(query: str, llm: LLMProvider) -> Dict[str, Any]:
    intent = llm.extract_retrieval_intent(query)
    name = (intent.get("patient_name") or "").strip()
    report_type = intent.get("report_type")

    if not name:
        return {
            "status": "not_found",
            "message": "I couldn't identify a patient name in your request. "
                       "Try: \"Open Priya Sharma's latest OPG report\".",
            "candidates": [], "evidence": [],
        }

    result = tools.search_patients(name)
    matches = result["patients"]

    if not matches:
        return {
            "status": "not_found",
            "message": f"No patient found matching '{name}'.",
            "candidates": [], "evidence": [],
        }

    if len(matches) > 1:
        return {
            "status": "ambiguous",
            "message": f"Multiple patients match '{name}'. Please specify:",
            "candidates": matches, "evidence": [],
        }

    patient = matches[0]
    report = tools.get_latest_report(patient["id"], report_type)
    if not report:
        label = f" {report_type}" if report_type else ""
        return {
            "status": "not_found",
            "patient": patient,
            "message": f"No{label} report found for {patient['name']}.",
            "candidates": [], "evidence": [],
        }

    return {
        "status": "found",
        "patient": patient,
        "report": report,
        "message": f"Latest{(' ' + report_type) if report_type else ''} "
                   f"report for {patient['name']} ({report['date']}).",
        "candidates": [],
        "evidence": [f"Report {report['id']} ({report['type']}, {report['date']})"],
    }
