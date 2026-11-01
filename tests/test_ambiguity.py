from app.services import retrieval
from app.llm.provider import get_llm

llm = get_llm()


def test_ambiguous_name_returns_candidates():
    r = retrieval.retrieve_report("Open Priya's latest report", llm)
    assert r["status"] == "ambiguous"
    assert len(r["candidates"]) == 2
    names = {p["name"] for p in r["candidates"]}
    assert names == {"Priya Sharma", "Priya Verma"}


def test_ambiguous_does_not_guess():
    r = retrieval.retrieve_report("Show me Priya latest OPG", llm)
    assert r["status"] == "ambiguous"
    assert r.get("report") is None
