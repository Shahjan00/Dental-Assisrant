import json
import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI


def _chat():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.environ["GEMINI_API_KEY"],
        temperature=0,
    )


def _clean(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z]*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
    return json.loads(raw)


def gemini_intent(query):
    prompt = (
        "Extract patient name and report type from this request. "
        'Reply ONLY JSON like {"patient_name": "...", "report_type": "OPG"}. '
        "Report type is OPG, IOPA, CBCT or null.\n\n" + query
    )
    return _clean(_chat().invoke(prompt).content)


def gemini_dictation(transcript):
    prompt = (
        "Convert this dental observation to JSON. Do NOT invent findings. "
        'Reply ONLY JSON like {"findings": [{"observation": "...", '
        '"anatomical_site": "...", "confidence": "medium", "requires_review": true}], '
        '"uncertainty_notes": []}.\n\n' + transcript
    )
    return _clean(_chat().invoke(prompt).content)


def gemini_followup(message, context):
    prompt = (
        "Answer using ONLY this report. If not in the report, say so. "
        'Reply ONLY JSON like {"reply": "...", "evidence": [...]}.\n\n'
        f"Report: {json.dumps(context.get('report', {}))}\nQuestion: {message}"
    )
    return _clean(_chat().invoke(prompt).content)
