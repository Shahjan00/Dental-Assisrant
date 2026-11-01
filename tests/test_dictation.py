from app.services import dictation
from app.llm.provider import get_llm

llm = get_llm()


def test_dictation_extracts_tooth():
    d = dictation.dictate("Lower right third molar (48) is horizontally impacted", llm)
    assert len(d["findings"]) == 1
    assert d["findings"][0]["anatomical_site"] == "Tooth 48"
    assert d["clinician_review_required"] is True


def test_uncertain_claims_flagged():
    d = dictation.dictate("Maybe there is possible bone loss, unclear", llm)
    assert d["findings"][0]["confidence"] == "low"
    assert len(d["uncertainty_notes"]) > 0


def test_empty_transcript():
    d = dictation.dictate("   ", llm)
    assert d["findings"] == []
    assert d["clinician_review_required"] is True
