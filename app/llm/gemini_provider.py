"""Gemini provider via LangChain. Requires GEMINI_API_KEY env var."""
import json
import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.llm.provider import LLMProvider


def _llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.environ["GEMINI_API_KEY"],
        temperature=0,
    )


_INTENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Extract the patient name and report type from a dental report request. "
     "Report types: OPG, IOPA, CBCT, or null if not mentioned. "
     "Reply ONLY with JSON: {{\"patient_name\": str|null, \"report_type\": str|null}}"),
    ("human", "{query}"),
])

_DICTATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a clinical documentation assistant. Convert the dentist's spoken "
     "observation into structured JSON. NEVER invent findings not stated. "
     "Flag uncertainty. Reply ONLY with JSON: "
     "{{\"findings\": [{{\"observation\": str, \"anatomical_site\": str|null, "
     "\"confidence\": \"high\"|\"medium\"|\"low\", \"requires_review\": true}}], "
     "\"uncertainty_notes\": [str]}}"),
    ("human", "{transcript}"),
])

_FOLLOWUP_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Answer the clinician's follow-up question using ONLY the provided report. "
     "If the answer is not in the report, say so explicitly. "
     "Reply ONLY with JSON: {{\"reply\": str, \"evidence\": [str]}}"),
    ("human", "Report: {report_json}\n\nQuestion: {message}"),
])


def _parse_json(raw: str) -> Dict[str, Any]:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z]*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
    return json.loads(raw)


import re  # noqa: E402  (kept at bottom to avoid circular import noise)


class GeminiProvider(LLMProvider):
    def extract_retrieval_intent(self, query: str) -> Dict[str, Any]:
        chain = _INTENT_PROMPT | _llm()
        return _parse_json(chain.invoke({"query": query}).content)

    def structure_dictation(self, transcript: str) -> Dict[str, Any]:
        chain = _DICTATION_PROMPT | _llm()
        return _parse_json(chain.invoke({"transcript": transcript}).content)

    def answer_followup(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        chain = _FOLLOWUP_PROMPT | _llm()
        return _parse_json(chain.invoke({
            "report_json": json.dumps(context.get("report", {})),
            "message": message,
        }).content)


def get_provider() -> LLMProvider:
    """Gemini when a key is present, otherwise the deterministic mock."""
    if os.environ.get("GEMINI_API_KEY"):
        return GeminiProvider()
    from app.llm.mock_provider import MockProvider
    return MockProvider()
