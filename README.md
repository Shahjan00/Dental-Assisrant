# Dental Assistant

Voice-first dental assistant PoC for the VI-SCAN Diagnostics AI Engineer take-home.

Three core features plus one bonus:

1. **Report retrieval** — natural language lookup ("Open Priya Sharma's latest OPG report"), with ambiguity and missing-data handling
2. **Dictation to draft** — clinical dictation → structured JSON (findings, anatomical site, uncertainty notes), always flagged for clinician review
3. **Follow-up chat** — session-aware Q&A grounded in the selected report, with evidence citations
4. **Bonus: report-aware chatbot** — `/api/chat` answers grounded questions about the loaded report

## Setup

### 1. Clone

```bash
git clone https://github.com/Shahjan00/Dental-Assisrant.git
cd Dental-Assisrant
```

### 2. Install

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment variables

Copy the sample and add your key:

```bash
cp .env.example .env
```

`.env.example`:

```
GEMINI_API_KEY=your_key_here
```

Without a key, the app runs on a built-in mock provider — all three endpoints still work, so reviewers can try everything without setup.

### 4. Run

```bash
uvicorn app.main:app --reload
```

Open http://localhost:8000 in the browser for the demo page, or http://localhost:8000/docs for the API.

### 5. Tests

```bash
pytest tests/ -v
```

8 tests covering retrieval, ambiguity, dictation, and chat.

## Model and provider choices

- **LLM: Gemini 1.5 Flash via `langchain-google-genai`.** Chosen for fast structured output and a generous free tier. The assignment asked for LangChain — I used `with_structured_output` with Pydantic schemas (`IntentOut`, `DictationOut`, `FollowupOut`) instead of prompt-hacking JSON out of raw text.
- **No LangGraph.** The flow is linear (parse → lookup → respond), so direct function calls are simpler and easier to follow than a graph. The architecture still keeps the key separation: the LLM never touches data directly.
- **Mock provider fallback.** `app/llm/mock_provider.py` is a rule-based stand-in used when no API key is set, or automatically per-request if a Gemini call fails (`fallback_used: true` in the response). This keeps the demo runnable for anyone.
- **Data: JSON files, not a database.** `app/data/patients.json` (6 patients) and `app/data/reports.json` (12 reports) — synthetic, as the brief requires. A real deployment would swap the store module for PostgreSQL; the lookup functions are plain and swappable.

## How it works

1. **Retrieve** (`POST /api/retrieve`): LLM extracts patient name + report type from the query → deterministic lookup in the JSON store → if multiple patients match, returns candidates instead of guessing → saves the result in a session.
2. **Dictate** (`POST /api/dictate`): LLM structures the transcript into findings with anatomical sites → flags low-confidence items → always returns `clinician_review_required: true`. Nothing is ever auto-finalized.
3. **Chat** (`POST /api/chat`): resolves follow-ups ("summarize her report") via the session from step 1 → LLM answers using only the loaded report → every answer includes evidence citations.

See `ARCHITECTURE.md` for the full one-page breakdown.

## Demo

Two ways to try it:

- **Browser demo page** at `/` — three sections (find a report, dictation, chat) hitting the API directly.
- **Documented API sequence** in `demo/api_examples.md` — step-by-step curl calls with sample outputs for all three features plus the bonus.

## Known limitations

- **No real voice input.** The brief allows mocked STT; the API accepts typed text as the transcript. A production version would pipe audio through Whisper first.
- **In-memory sessions.** Session state resets on restart — fine for a demo, needs Redis or similar in production.
- **Mock provider is keyword-based.** It handles common phrasings but won't parse everything; the Gemini path is the real implementation.
- **No auth.** No login, no audit trail — a clinical tool handling real PHI would need both.
- **Synthetic data only.** 6 patients, 12 reports — enough to demo every scenario (ambiguity, missing report, uncertainty), not a real dataset.
