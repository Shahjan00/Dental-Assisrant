# Dental Assistant

Voice-first dental assistant PoC. Takes typed or spoken requests like
"Open Priya's latest OPG report" and clinical dictations, returns
structured data. Built for the VI-SCAN AI Engineer take-home.

## Setup

```bash
pip install -r requirements.txt

# optional: for real LLM calls
cp .env.example .env
# put your Gemini key in .env

uvicorn app.main:app --reload
```

Without a Gemini key it runs on a built-in rule-based mock, so it works out of the box.

## API

- `POST /api/retrieve` - find a patient report
  ```json
  {"query": "Open Priya Sharma's latest OPG report"}
  ```
- `POST /api/dictate` - transcript to structured draft
  ```json
  {"transcript": "Lower right third molar (48) is horizontally impacted"}
  ```
- `POST /api/chat` - follow-up questions (needs session_id from /api/retrieve)
  ```json
  {"message": "Summarize her report", "session_id": "..."}
  ```

## Tests

```bash
pytest tests/ -v
```

## Known limitations

- STT is mocked (typed input). The pipeline accepts a transcript string where audio would go.
- Mock LLM handles common patterns; edge-case phrasing may miss. Gemini handles the rest.
- Session memory is in-memory only, resets on restart.
- All patient data is synthetic.
