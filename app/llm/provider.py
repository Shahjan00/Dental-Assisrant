# pick gemini if key exists, else use mock
import os


def get_llm():
    if os.environ.get("GEMINI_API_KEY"):
        from app.llm.gemini_provider import gemini_intent, gemini_dictation, gemini_followup
        return {
            "intent": gemini_intent,
            "dictation": gemini_dictation,
            "followup": gemini_followup,
            "name": "gemini",
        }
    from app.llm.mock_provider import mock_intent, mock_dictation, mock_followup
    return {
        "intent": mock_intent,
        "dictation": mock_dictation,
        "followup": mock_followup,
        "name": "mock",
    }
