import json
import os

base = os.path.dirname(__file__)

with open(os.path.join(base, "patients.json")) as f:
    patients = json.load(f)

with open(os.path.join(base, "reports.json")) as f:
    reports = json.load(f)


def find_patients(name):
    q = name.lower().strip()
    return [p for p in patients if q in p["name"].lower()]


def get_patient(pid):
    for p in patients:
        if p["id"] == pid:
            return p
    return None


def get_reports(pid):
    return [r for r in reports if r["patient_id"] == pid]


def latest_report(pid, rtype=None):
    rs = get_reports(pid)
    if rtype:
        rs = [r for r in rs if r["type"] == rtype.upper()]
    if not rs:
        return None
    return sorted(rs, key=lambda x: x["date"], reverse=True)[0]
