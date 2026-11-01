from app.data import store


def search_patients(name):
    matches = store.find_patients(name)
    return {"count": len(matches), "patients": matches}


def get_patient(pid):
    return store.get_patient(pid)


def get_latest_report(pid, rtype=None):
    return store.latest_report(pid, rtype)


def get_patient_reports(pid):
    return store.get_reports(pid)
