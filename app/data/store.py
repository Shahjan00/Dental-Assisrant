"""Data access layer. JSON-backed today; swap for PostgreSQL via this interface."""
import json
import os
from typing import List, Optional
from app.models import Patient, Report

_DATA_DIR = os.path.join(os.path.dirname(__file__))


def _load(filename: str):
    path = os.path.join(_DATA_DIR, filename)
    with open(path) as f:
        return json.load(f)


class PatientStore:
    """Repository for patient records."""

    def __init__(self):
        self._patients: List[Patient] = [
            Patient(**p) for p in _load("patients.json")
        ]

    def search_by_name(self, name: str) -> List[Patient]:
        """Case-insensitive substring match on patient name."""
        q = name.strip().lower()
        return [p for p in self._patients if q in p.name.lower()]

    def get_by_id(self, patient_id: str) -> Optional[Patient]:
        for p in self._patients:
            if p.id == patient_id:
                return p
        return None

    def all(self) -> List[Patient]:
        return list(self._patients)


class ReportStore:
    """Repository for clinical reports."""

    def __init__(self):
        self._reports: List[Report] = [
            Report(**r) for r in _load("reports.json")
        ]

    def for_patient(self, patient_id: str) -> List[Report]:
        return [r for r in self._reports if r.patient_id == patient_id]

    def latest(self, patient_id: str, report_type: Optional[str] = None) -> Optional[Report]:
        reports = self.for_patient(patient_id)
        if report_type:
            reports = [r for r in reports if r.type == report_type.upper()]
        if not reports:
            return None
        return sorted(reports, key=lambda r: r.date, reverse=True)[0]

    def get_by_id(self, report_id: str) -> Optional[Report]:
        for r in self._reports:
            if r.id == report_id:
                return r
        return None
