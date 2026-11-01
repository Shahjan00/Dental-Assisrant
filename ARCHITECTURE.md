# Architecture

## Flow

```
User query/transcript
       |
       v
  FastAPI (/api/retrieve, /api/dictate, /api/chat)
       |
       v
  LLM layer (intent extraction / structuring)
  - Gemini via LangChain (with_structured_output) if API key set
  - Rule-based mock otherwise
       |
       v
  Deterministic tools (clinical_tools.py)
  - search_patients, get_latest_report, etc.
  - Business rules live here: ambiguity -> ask, never guess
       |
       v
  Services (retrieval.py, dictation.py, conversation.py)
  - Combine LLM output + tool results
  - conversation.py keeps session memory for follow-ups
       |
       v
  JSON response (always cites source report as evidence)
```

## Key decisions

- **LLM never touches data directly.** It extracts intent / structures text,
  then deterministic functions do the actual lookup. This keeps the LLM from
  hallucinating patient records.
- **Ambiguity is a first-class result.** Two patients named Priya ->
  return both and ask, instead of picking one.
- **Every answer cites evidence.** Each response includes the report ID,
  type, and date it came from.
- **Uncertainty is labeled.** Dictation output flags confidence per finding
  and always requires clinician review.

## Production considerations

- **Data**: JSON files work for a PoC. Production would use PostgreSQL
  behind the same store interface.
- **Privacy**: Real deployment needs auth, audit logging, and encryption
  for PHI. This demo uses synthetic data only.
- **Latency/cost**: Gemini flash is cheap and fast. Cache frequent
  lookups. The mock provider costs nothing.
- **STT**: Swap the transcript string input for Whisper or Google STT;
  the pipeline already accepts text where audio would plug in.
