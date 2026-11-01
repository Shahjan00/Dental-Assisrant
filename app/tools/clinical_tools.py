"""Deterministic clinical tools. The LLM calls these; business rules live here, not in prompts."""
from typing import List, Optional, Dict, Any
from app.models import Patient, Report
from app.data.store import PatientStore, ReportStore

_patient_store = PatientStore()
_report_store = ReportStore()


def search_patients(name: str) -> Dict[str, Any]:
    """Search patients by name. Returns matches; caller must handle ambiguity."""
    matches = _patient_store.search_by_name(name)
    return {
        "count": len(matches),
        "patients": [p.model_dump() for p in matches],
    }


def get_patient(patient_id: str) -> Optional[Dict[str, Any]]:
    p = _patient_store.get_by_id(patient_id)
    return p.model_dump() if p else None


def get_latest_report(patient_id: str, report_type: Optional[str] = None) -> Optional[Dict[str, Any]]:
    r = _report_store.latest(patient_id, report_type)
    return r.model_dump() if r else None


def get_patient_reports(patient_id: str) -> List[Dict[str, Any]]:
    return [r.model_dump() for r in _report_store.for_patient(patient_id)]


def get_report(report_id: str) -> Optional[Dict[str, Any]]:
    r = _report_store.get_by_id(report_id)
    return r.model_dump() if r else None
