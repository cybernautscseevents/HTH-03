# ClinScribe AI — REST API Reference

> Base URL: `http://localhost:8000` (or `http://localhost:8000/api`)  
> Interactive OpenAPI / Swagger UI: `http://localhost:8000/docs`

---

## 1. Authentication (`/auth`)

### `POST /auth/login`
Authenticates a healthcare practitioner and returns a JWT Bearer token.

**Request:**
```json
{
  "email": "dr.priya@clinscribe.demo",
  "password": "demo123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "user-demo-001",
    "email": "dr.priya@clinscribe.demo",
    "full_name": "Dr. Priya Sharma",
    "role": "doctor"
  }
}
```

---

## 2. Patients (`/patients`)

### `GET /patients`
Search and list registered OPD patients.
- Query Parameters: `search` (string, optional), `limit` (int, default 20), `offset` (int, default 0)

### `GET /patients/{id}`
Fetch detailed patient demographic and clinical registration record by ID.

### `GET /patients/{id}/timeline`
Retrieve longitudinal chronological encounters, previous diagnoses, and prescription history.

---

## 3. Consultations (`/consultations`)

### `POST /consultations`
Create a new OPD encounter session with explicit DPDP consent status.

### `GET /consultations/{id}`
Fetch encounter details, associated patient metadata, specialty, and session status.

### `POST /consultations/{id}/start`
Initiate ambient recording session. Sets status to `in_progress`.

### `POST /consultations/{id}/stop`
Terminates recording session and queues audio buffer for ASR and Clinical NLP synthesis.

### `GET /consultations/{id}/transcript`
Fetch speaker-diarized multilingual transcript turns with timestamps, original Indic text, and English translations.

### `GET /consultations/{id}/clinical-note`
Retrieve the latest AI-generated or doctor-approved clinical documentation.

### `GET /consultations/{id}/evidence`
Fetch all bidirectional grounding links connecting clinical entities to dialogue turns.

### `GET /consultations/{id}/safety-flags` (or `/safety-check`)
Retrieve real-time safety guardrail warnings (allergies, red flags, contraindications).

### `GET /consultations/{id}/patient-summary`
Retrieve multilingual patient discharge summary leaflet in Kannada, Hindi, and English.

---

## 4. Clinical Processing (`/clinical`)

### `POST /clinical/extract`
Extracts structured clinical entities (symptoms, vitals, medications, absent findings) from transcript segments.

### `POST /clinical/generate-note`
Synthesizes structured SOAP note draft from extracted entities using specialty-aware templates.

### `POST /clinical/{note_id}/approve`
Physician electronic approval or rejection of clinical note.

**Request:**
```json
{
  "action": "approve",
  "reason": null
}
```

### `GET /clinical/{note_id}/evidence`
Query evidence links for a specific note, with optional filter by `field_path`.

---

## 5. ABDM Interoperability & FHIR (`/encounters`)

### `GET /encounters/{id}/fhir`
Exports encounter in HL7 FHIR R4 document bundle conforming to ABDM NRCES profile:
- Contained resources: `Patient`, `Practitioner`, `Encounter`, `Condition`, `MedicationRequest`.

---

## 6. Evaluation & Governance (`/evaluation`, `/privacy`)

### `GET /evaluation/metrics` (or `/evaluation/dashboard`)
Retrieves quantitative performance metrics:
- ASR WER / CER across Indian languages
- Clinical NLP extraction Precision, Recall, F1
- OPD documentation time saved (baseline vs ambient)
- Unsupported information rate (hallucination rate = 0.0%)

### `GET /privacy`
Returns privacy governance status, PII masking configuration, and data retention policies.

### `GET /health`
System health check endpoint returning service version and operational mode.
