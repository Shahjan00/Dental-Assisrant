from app.tools import clinical_tools as tools


def retrieve_report(query, llm):
    intent = llm["intent"](query)
    name = (intent.get("patient_name") or "").strip()
    rtype = intent.get("report_type")

    if not name:
        return {"status": "not_found",
                "message": "Couldn't find a patient name. Try \"Open Priya Sharma's latest OPG report\".",
                "candidates": [], "evidence": []}

    matches = tools.search_patients(name)["patients"]

    if not matches:
        return {"status": "not_found",
                "message": f"No patient matching '{name}'.",
                "candidates": [], "evidence": []}

    if len(matches) > 1:
        names = ", ".join(p["name"] for p in matches)
        return {"status": "ambiguous",
                "message": f"Found multiple: {names}. Which one?",
                "candidates": matches, "evidence": []}

    patient = matches[0]
    report = tools.get_latest_report(patient["id"], rtype)

    if not report:
        label = f" {rtype}" if rtype else ""
        return {"status": "not_found", "patient": patient,
                "message": f"No{label} report for {patient['name']}.",
                "candidates": [], "evidence": []}

    return {"status": "found", "patient": patient, "report": report,
            "message": f"Latest report for {patient['name']} ({report['date']}).",
            "candidates": [],
            "evidence": [f"Report {report['id']} ({report['type']}, {report['date']})"]}
