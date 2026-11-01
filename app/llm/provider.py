import os


def _mock():
    from app.llm.mock_provider import mock_intent, mock_dictation, mock_followup
    return {
        "intent": mock_intent,
        "dictation": mock_dictation,
        "followup": mock_followup,
        "name": "mock",
    }


def _gemini():
    from app.llm.gemini_provider import gemini_intent, gemini_dictation, gemini_followup
    return {
        "intent": gemini_intent,
        "dictation": gemini_dictation,
        "followup": gemini_followup,
        "name": "gemini",
    }


def get_llm():
    if os.environ.get("GEMINI_API_KEY"):
        return _gemini()
    return _mock()


def safe_call(llm, fn_name, *args, **kwargs):
    """Try primary LLM, fall back to mock on any failure."""
    try:
        return llm[fn_name](*args, **kwargs), False
    except Exception as e:
        print(f"LLM {fn_name} failed ({e}), falling back to mock")
        mock = _mock()
        return mock[fn_name](*args, **kwargs), True
