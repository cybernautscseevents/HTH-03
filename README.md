# ClinScribe AI

> **"From Conversation to Clinical Intelligence."**

ClinScribe AI is an AI-powered ambient clinical intelligence platform designed for Indian outpatient departments (OPDs). It listens to doctor-patient consultations, understands Indian multilingual and code-mixed conversations, identifies clinically relevant information, and converts conversations into structured, evidence-linked clinical documentation — while keeping the doctor in complete control.

## ⚕️ Disclaimer

> **Prototype demonstration uses synthetic patient data. Not intended for autonomous medical diagnosis or treatment. The doctor remains the final decision-maker.**

## Problem

Indian doctors in busy OPDs handle large patient volumes while simultaneously listening, diagnosing, and documenting. Consultations frequently involve code-mixed speech (e.g., Kannada + English), making generic speech-to-text systems inadequate.

## Solution

ClinScribe AI transforms natural Indian OPD conversations into accurate, structured, traceable, doctor-verified clinical documentation through:

1. **Bharat-first multilingual/code-mixed understanding** — Kannada, Hindi, Tamil, Telugu, Malayalam + English
2. **Clinical structure and entity extraction** — symptoms, vitals, medications, negation detection
3. **Evidence-linked AI outputs** — every AI-generated field traces back to the original conversation
4. **Doctor-in-the-loop safety** — AI output is always a draft; doctor reviews, edits, and approves
5. **Interoperable healthcare-ready data** — FHIR-compatible structured output

## Core Flow

```
Doctor Login → Select Patient → Start Consultation → Live Audio Capture
→ Speaker Diarization → Indian Multilingual ASR → Code-Mixed Language Processing
→ Clinical Entity Extraction → Clinical Note Generation → Safety Validation
→ Evidence Linking → Doctor Review → Doctor Approval → Final Clinical Record
→ Patient-Friendly Summary → FHIR-ready Export
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, shadcn/ui, Framer Motion |
| Backend | Python 3.11, FastAPI, Pydantic v2 |
| Database | PostgreSQL 15, SQLAlchemy 2.0 |
| Cache | Redis |
| ASR | AI4Bharat IndicConformer (primary), Whisper (fallback) |
| NLP | spaCy, custom clinical extraction pipeline |
| Auth | JWT + bcrypt |
| Deployment | Docker, docker-compose |

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (optional, demo mode uses in-memory store)
- Redis (optional)

### Backend

```bash
cd apps/api
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
cp ../../.env.example .env

# Start the API server
python main.py
```

Backend runs at: http://localhost:8000
API docs: http://localhost:8000/docs

### Frontend

```bash
cd apps/web
npm install
npm run dev
```

Frontend runs at: http://localhost:3000

### Demo Credentials

- Email: `dr.priya@clinscribe.demo`
- Password: `demo123`

## Demo Mode

ClinScribe AI includes a full demo mode with pre-recorded synthetic consultations. This guarantees a reliable presentation even if external AI services are unavailable.

To run the demo pipeline:
1. Login with demo credentials
2. Navigate to Dashboard
3. Select "Demo Consultation — General Medicine"
4. Click "Run Pipeline"
5. Review the generated clinical note, evidence links, and safety flags

## Project Structure

```
clinscribe-ai/
├── apps/
│   ├── web/           # Next.js frontend
│   └── api/           # FastAPI backend
├── services/
│   ├── asr/           # Speech recognition service
│   ├── diarization/   # Speaker diarization
│   ├── clinical-nlp/  # Clinical NLP pipeline
│   ├── safety/        # Clinical safety guard
│   ├── evidence/      # Evidence linking engine
│   └── fhir/          # FHIR export service
├── datasets/
│   ├── synthetic/     # Synthetic demo data
│   └── evaluation/    # Evaluation test cases
├── docs/              # Documentation
├── tests/             # Test suites
└── docker/            # Docker configuration
```

## API Documentation

See [API.md](docs/API.md) for complete API reference.

Key endpoints:
- `POST /auth/login` — Authentication
- `GET /patients` — Patient search
- `POST /consultations` — Create consultation
- `POST /audio/transcribe` — Transcribe audio
- `POST /clinical/extract` — Extract clinical entities
- `POST /clinical/generate-note` — Generate clinical note
- `POST /clinical/validate` — Safety validation
- `GET /clinical/{id}/evidence` — Evidence links
- `POST /clinical/{id}/approve` — Doctor approval

## Key Features

- **Live Ambient Audio** — Professional consultation recording interface
- **Speaker Diarization** — Doctor/Patient/Other speaker separation
- **Indian Multilingual ASR** — Kannada, Hindi, Tamil, Telugu, Malayalam + English
- **Code-Mixed Understanding** — Clinical meaning from mixed-language speech
- **Clinical Entity Extraction** — Symptoms, vitals, medications, allergies, negation
- **Negation Detection** — "No chest pain" → Chest pain: ABSENT
- **Structured Clinical Notes** — OPD note generation with specialty templates
- **Evidence-Linked AI** — Every field traces to source transcript
- **Clinical Safety Guard** — Missing info, dosage safety, hallucination detection
- **Doctor-in-the-Loop** — AI draft → Review → Edit → Approve → Final
- **Patient-Friendly Summary** — Simple visit summary in patient's language
- **Patient Timeline** — Longitudinal health record
- **FHIR-Ready Export** — Healthcare interoperability
- **Evaluation Dashboard** — ASR WER, extraction precision/recall/F1

## License

MIT License. See [LICENSE](LICENSE).

## Open Source

See [OPEN_SOURCE_NOTICES.md](OPEN_SOURCE_NOTICES.md) for attribution.
