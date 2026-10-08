# ClinScribe AI — Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ClinScribe AI Platform                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────────┐   │
│  │  Next.js     │    │   FastAPI     │    │  PostgreSQL   │   │
│  │  Frontend    │◄──►│   Backend     │◄──►│   Database    │   │
│  │  (Port 3000) │    │  (Port 8000)  │    │  (Port 5432)  │   │
│  └─────────────┘    └──────┬───────┘    └───────────────┘   │
│                            │                                  │
│                     ┌──────┴───────┐                         │
│                     │  AI Pipeline  │                         │
│                     └──────┬───────┘                         │
│                            │                                  │
│         ┌──────────────────┼──────────────────┐              │
│         ▼                  ▼                  ▼              │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐      │
│  │     ASR      │  │  Clinical    │  │    Safety     │      │
│  │   Service    │  │  NLP Engine  │  │    Guard      │      │
│  └──────┬──────┘  └──────┬───────┘  └───────────────┘      │
│         │                │                                    │
│    ┌────┴────┐    ┌──────┴───────┐                           │
│    ▼         ▼    ▼              ▼                           │
│ ┌──────┐ ┌─────┐ ┌──────┐ ┌────────┐                       │
│ │Indic │ │Whis-│ │Entity│ │Evidence│                        │
│ │Conf. │ │per  │ │Extr. │ │Linking │                        │
│ └──────┘ └─────┘ └──────┘ └────────┘                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## AI Pipeline Architecture

```
Audio Input
    │
    ▼
┌───────────────────────────────┐
│ ASR Abstraction Layer          │
│ ┌───────────────┐             │
│ │ IndicConformer │ (Primary)   │
│ ├───────────────┤             │
│ │ Whisper        │ (Fallback)  │
│ ├───────────────┤             │
│ │ Demo Provider  │ (Reliable)  │
│ └───────────────┘             │
└───────────┬───────────────────┘
            │ Raw Transcript
            ▼
┌───────────────────────────────┐
│ Speaker Diarization            │
│ Doctor / Patient / Other       │
└───────────┬───────────────────┘
            │ Attributed Segments
            ▼
┌───────────────────────────────┐
│ Code-Mixed Language Processing │
│ Kannada+English, Hindi+English │
│ Preserve original + translate  │
└───────────┬───────────────────┘
            │ Processed Segments
            ▼
┌───────────────────────────────┐
│ Clinical Entity Extraction     │
│ • Symptoms                     │
│ • Vitals                       │
│ • Medications                  │
│ • Negation Detection           │
│ • Duration/Severity            │
└───────────┬───────────────────┘
            │ Structured Entities
            ▼
┌───────────────────────────────┐
│ Clinical Note Generation       │
│ Specialty-aware templates      │
│ Structured JSON output         │
└───────────┬───────────────────┘
            │
     ┌──────┴──────┐
     ▼             ▼
┌─────────┐  ┌──────────┐
│ Safety  │  │ Evidence │
│ Guard   │  │ Linking  │
└────┬────┘  └────┬─────┘
     │            │
     └──────┬─────┘
            ▼
┌───────────────────────────────┐
│ Doctor Review Interface        │
│ AI Draft → Review → Approve    │
└───────────────────────────────┘
```

## Data Flow

### Clinical Note Status Machine

```
AI_GENERATED → NEEDS_REVIEW → VERIFIED → FINAL
                    ↓
                 REJECTED
```

### Security Layers

```
Client Request
    │
    ▼
[HTTPS/TLS]
    │
    ▼
[JWT Authentication]
    │
    ▼
[Role-Based Access Control]
    │
    ▼
[Input Validation (Pydantic)]
    │
    ▼
[Business Logic]
    │
    ▼
[Audit Logging]
    │
    ▼
[Database (Encrypted)]
```

## Database Schema

Core entities and relationships:

- **Users** → Doctors (1:1)
- **Doctors** → Consultations (1:N)
- **Patients** → Consultations (1:N)
- **Consultations** → Audio Sessions (1:1)
- **Consultations** → Transcript Segments (1:N)
- **Consultations** → Clinical Entities (1:N)
- **Consultations** → Clinical Notes (1:N)
- **Clinical Notes** → Note Versions (1:N)
- **Clinical Notes** → Evidence Links (1:N)
- **Consultations** → Safety Flags (1:N)
- **Patients** → Timeline Entries (1:N)

## Key Design Decisions

1. **In-memory store for demo**: Enables running without PostgreSQL during hackathon
2. **Modular ASR**: Factory pattern allows provider switching without code changes
3. **Evidence-first extraction**: Source segment IDs embedded in every entity from extraction time
4. **Safety checks are rule-based**: Deterministic safety validation, not AI-dependent
5. **Version history**: Clinical notes maintain full version trail
6. **Audit logging**: Every significant action is logged with user, timestamp, and details
