from app.services import retrieval
from app.llm.provider import get_llm

llm = get_llm()


def test_exact_retrieval():
    r = retrieval.retrieve_report("Open Priya Sharma's latest OPG report", llm)
    assert r["status"] == "found"
    assert r["patient"]["name"] == "Priya Sharma"
    assert r["report"]["type"] == "OPG"
    assert r["report"]["id"] == "R001"


def test_retrieval_with_type_filter():
    r = retrieval.retrieve_report("Show Rahul Mehta's IOPA", llm)
    assert r["status"] == "found"
    assert r["report"]["type"] == "IOPA"


def test_patient_not_found():
    r = retrieval.retrieve_report("Open John Doe's report", llm)
    assert r["status"] == "not_found"
