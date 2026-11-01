# Dental Assistant

Voice-first dental assistant PoC for VI-SCAN Diagnostics.

## Demo

Open the app in your browser — a simple demo page at `/` with three sections:
1. **Find a report** — type "Open Priya Sharma's latest OPG report"
2. **Dictation** — paste clinical dictation, get structured JSON draft
3. **Follow-up chat** — ask questions about the loaded report (uses the session from step 1)

Or use the API directly — see `demo/api_examples.md`.

## Features

- **Report retrieval** (`POST /api/retrieve`): natural language lookup with ambiguity handling
- **Dictation** (`POST /api/dictate`): clinical text → structured JSON (findings, anatomical site, uncertainty notes)
- **Follow-up chat** (`POST /api/chat`): session-aware Q&A grounded in the selected report — *bonus feature*

All responses cite evidence and flag uncertainty. If the LLM call fails mid-request, the endpoint falls back to the local mock provider and marks `fallback_used: true`.

## Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Run

```bash
uvicorn app.main:app --reload
```

Then open http://localhost:8000 in your browser.
