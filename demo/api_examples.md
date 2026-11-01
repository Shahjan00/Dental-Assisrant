# Demo: API walkthrough

Base URL: `http://localhost:8000`

## 1. Retrieve a report

```bash
curl -X POST http://localhost:8000/api/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query": "Open Priya Sharma'"'"'s latest OPG report"}'
```

Response (abbreviated):
```json
{
  "session_id": "a1b2c3d4-...",
  "status": "found",
  "patient": {"id": "P001", "name": "Priya Sharma", "age": 28},
  "report": {
    "id": "R001", "type": "OPG", "date": "2026-10-15",
    "findings": ["Lower right third molar (48) is horizontally impacted..."]
  },
  "evidence": ["Report R001 (OPG, 2026-10-15)"]
}
```

## 2. Ambiguous name

```bash
curl -X POST http://localhost:8000/api/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me Priya'"'"'s latest report"}'
```

```json
{
  "status": "ambiguous",
  "message": "Found multiple: Priya Sharma, Priya Verma. Which one?",
  "candidates": [...]
}
```

## 3. Dictation to draft

```bash
curl -X POST http://localhost:8000/api/dictate \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Lower right third molar (48) is horizontally impacted"}'
```

```json
{
  "findings": [{
    "observation": "Lower right third molar (48) is horizontally impacted",
    "anatomical_site": "Tooth 48",
    "confidence": "medium",
    "requires_review": true
  }],
  "draft_report": "DRAFT REPORT (needs clinician review)\n\n1. [Tooth 48] Lower right third molar (48) is horizontally impacted",
  "clinician_review_required": true
}
```

## 4. Follow-up (use session_id from step 1)

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Summarize her report", "session_id": "a1b2c3d4-..."}'
```

```json
{
  "reply": "Summary of OPG (2026-10-15): Lower right third molar (48) is horizontally impacted...",
  "evidence": ["Lower right third molar (48) is horizontally impacted..."]
}
```
