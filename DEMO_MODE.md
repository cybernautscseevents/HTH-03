# ClinScribe AI — Demo Mode & Offline Operation

> **"From Conversation to Clinical Intelligence."**  
> Problem Statement: HC-02 — Ambient Clinical Scribe for Indian OPDs

---

## 1. Overview

**Demo Mode** in ClinScribe AI is a deterministic, offline-capable execution environment designed for:
- Hackathon demonstrations & jury evaluations
- Environments without active internet or GPU infrastructure
- Reproducible testing of multilingual clinical entity extraction, evidence grounding, and safety guardrails
- Absolute privacy compliance using **synthetic patient data** with zero risk of PHI leakage

Demo Mode is **not** a mock wireframe. It executes the real application logic:
- Real FastAPI routes and SQLAlchemy database models
- Real deterministic Clinical NLP pipeline with negation handling
- Real rule-based clinical safety engine (drug allergies, contraindications, red flags)
- Real bidirectional evidence grounding engine
- Real ABDM NRCES-compliant HL7 FHIR R4 Bundle generation

---

## 2. Configuration & Activation

Demo Mode is controlled via the environment variable in `.env`:

```bash
# Enable Demo Mode
DEMO_MODE=true
ASR_PROVIDER=demo
LLM_PROVIDER=demo
```

When `DEMO_MODE=true`:
1. The backend loads synthetic outpatient consultation records (e.g. `consult-demo-001`).
2. Audio transcription uses deterministic, high-fidelity dialogue turns modeled on AI4Bharat IndicConformer outputs.
3. Clinical extraction executes deterministic entity linking and negation detection.
4. No external API keys (OpenAI/Anthropic/Gemini) are required.

---

## 3. Demo Consultation Scenario (Kannada + English Code-Mixed)

| Dimension | Details |
| :--- | :--- |
| **Patient** | Rahul Kumar (42M, MRN-2026-0001) |
| **ABHA ID** | `91-8822-4411-9988` |
| **Language Register** | Kannada-English code-mixed (*Kanglish*) |
| **Chief Complaint** | Fever of 3 days duration (*"3 dinadinda tumba jwara ide"*) |
| **Associated Symptoms** | Nocturnal dry cough (*"Kasa kasa kheduttide, ratri jaasti"*), rhinorrhea, myalgia |
| **Pertinent Negatives** | No chest pain (*"edeya novu illa"*), no breathlessness (*"usiru kattuvike illa"*) |
| **Vitals** | Blood Pressure: 140/90 mmHg (elevated), Temperature: 101.5°F |
| **Documented Allergy** | Penicillin (historical chart record) |
| **Prescription Orders** | Tab. Paracetamol 500mg TDS x 3 days, Cough syrup 5ml BD x 5 days |

---

## 4. Key Interactive Flows to Demonstrate

1. **Ambient Recording Simulation**:
   - In the frontend (`http://localhost:3000`), click **"Run Ambient OPD Demo"**.
   - Observe live waveform animation, audio scrubber (02:45 total duration), and audio speed controls.
2. **Multilingual Transcript Stream**:
   - Inspect dialogue turns with speaker diarization badges (`Doctor` vs `Patient`).
   - Toggle between **Original Kannada/Mixed** and **English Translation**.
3. **"WHY?" Explainability Action**:
   - In the **Structured Clinical Note**, click the **"WHY?"** button on any extracted fact (e.g. Fever, Nocturnal Cough, Absent Chest Pain).
   - The **Evidence Inspector** flies out from the right, showing the verbatim audio transcript segment, confidence score (e.g. 96%), and timestamp bookmark.
4. **Clinical Safety Guardrails**:
   - Notice the **2 Flags** warning badge.
   - Click to review the Penicillin allergy cross-check alert and elevated BP observation.
5. **Patient Discharge Leaflet**:
   - Click **"Leaflet"** in the top action bar to inspect discharge instructions in **ಕನ್ನಡ (Kannada)**, **हिंदी (Hindi)**, and **English**.
6. **Patient Timeline & Compare Visits**:
   - Click the **"Patient Timeline"** tab in the navigation bar.
   - Inspect longitudinal encounters from May 2026, Sept 2026, and today.
   - Click **"Compare Visits"** for side-by-side comparison of blood pressure trends and symptom resolution.
7. **ABDM / FHIR R4 Bundle Export**:
   - Click **"ABDM FHIR"** in the top navigation to view and export the HL7 FHIR R4 document bundle conforming to the NRCES specification.

---

## 5. Offline Low-Connectivity Architecture

For Indian rural or semi-urban OPDs with intermittent internet:
- **Local Audio Buffering**: Web Audio API captures audio in local memory buffers.
- **Session Cache**: Consultations and notes persist in local SQLite / IndexedDB.
- **Graceful Fallback**: If external cloud ASR or LLM times out, the local heuristic pipeline automatically synthesizes notes and queues synchronization.
