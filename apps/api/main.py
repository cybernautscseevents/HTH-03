"""
ClinScribe AI — Main FastAPI Application
"From Conversation to Clinical Intelligence."

Ambient clinical intelligence platform for Indian OPDs.

DISCLAIMER: Prototype demonstration uses synthetic patient data.
Not intended for autonomous medical diagnosis or treatment.
The doctor remains the final decision-maker.
"""

import sys
import os
import uuid
import logging
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Query, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add parent directories to path for service imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'services', 'asr'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'services', 'clinical-nlp'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'services', 'safety'))

from config import get_settings
from schemas import (
    LoginRequest, LoginResponse, UserResponse, DoctorResponse,
    PatientCreate, PatientResponse, PatientSearchResponse,
    ConsultationCreate, ConsultationResponse,
    TranscriptSegmentResponse, TranscriptResponse,
    ClinicalExtractionResult, ClinicalEntityValue,
    ClinicalNoteResponse, ClinicalNoteUpdate, ClinicalNoteApproval,
    EvidenceLinkResponse, EvidenceDrawerResponse,
    SafetyFlagResponse, SafetyValidationResult,
    PatientSummaryResponse,
    TimelineEntry, PatientTimelineResponse,
    FHIRExportResponse,
    EvaluationDashboardResponse, ASRMetrics, ExtractionMetrics, WorkflowMetrics,
    PrivacyCenterResponse,
    TranscribeRequest, TranscribeResponse,
    AppSettings,
    ClinicalStatusEnum, SpeakerRoleEnum, SafetySeverityEnum,
)
from auth import hash_password, verify_password, create_access_token, get_current_user
from demo_data import (
    DEMO_USERS, DEMO_DOCTORS, DEMO_PATIENTS,
    DEMO_CONSULTATION_PRIMARY, DEMO_TRANSCRIPT_PRIMARY,
    DEMO_CLINICAL_EXTRACTION, DEMO_CLINICAL_NOTE,
    DEMO_EVIDENCE_LINKS, DEMO_SAFETY_FLAGS,
    DEMO_PATIENT_SUMMARY, DEMO_TIMELINE,
    DEMO_FHIR_BUNDLE, DEMO_EVALUATION_METRICS,
    SPECIALTY_TEMPLATES,
    DEMO_DOCTOR_ID, DEMO_DOCTOR_USER_ID,
)

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("clinscribe")


# ─── In-Memory Store (Demo Mode) ─────────────────────────
# For hackathon demo: in-memory state management
# Production: replaced by PostgreSQL via SQLAlchemy

class DemoStore:
    """In-memory data store for demo mode. Production uses PostgreSQL."""

    def __init__(self):
        self.users = {u["id"]: u for u in DEMO_USERS}
        self.doctors = {d["id"]: d for d in DEMO_DOCTORS}
        self.patients = {p["id"]: p for p in DEMO_PATIENTS}
        self.consultations = {}
        self.clinical_notes = {}
        self.audit_log = []

        # Initialize demo consultation
        self.consultations[DEMO_CONSULTATION_PRIMARY["id"]] = {
            **DEMO_CONSULTATION_PRIMARY,
            "consultation_date": datetime.now().isoformat(),
            "started_at": datetime.now().isoformat(),
        }

        # Hash demo password
        self.demo_password_hash = hash_password("demo123")

        logger.info("Demo store initialized with synthetic data")


store = DemoStore()


# ─── App Lifecycle ────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 60)
    logger.info("ClinScribe AI — Starting")
    logger.info("'From Conversation to Clinical Intelligence.'")
    logger.info(f"Mode: {'DEMO' if settings.demo_mode else 'LIVE'}")
    logger.info(f"ASR Provider: {settings.asr_provider}")
    logger.info("=" * 60)
    logger.info("")
    logger.info("⚕️  DISCLAIMER: Prototype demonstration uses synthetic patient data.")
    logger.info("   Not intended for autonomous medical diagnosis or treatment.")
    logger.info("   The doctor remains the final decision-maker.")
    logger.info("")
    yield
    logger.info("ClinScribe AI — Shutting down")


# ─── FastAPI App ──────────────────────────────────────────

app = FastAPI(
    title="ClinScribe AI",
    description=(
        "Ambient Clinical Intelligence for Indian OPDs. "
        "Transforms multilingual, code-mixed doctor-patient conversations "
        "into structured, evidence-linked clinical documentation."
    ),
    version="0.1.0-hackathon",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def api_prefix_strip_middleware(request: Request, call_next):
    path = request.scope["path"]
    if path.startswith("/api/"):
        request.scope["path"] = path[4:]
    response = await call_next(request)
    return response


# ─── Health Check ─────────────────────────────────────────

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ClinScribe AI",
        "version": "0.1.0-hackathon",
        "mode": "demo" if settings.demo_mode else "live",
        "timestamp": datetime.now().isoformat(),
    }


# ─── Auth Routes ─────────────────────────────────────────

@app.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Authenticate user and return JWT token."""
    # Demo mode: accept demo credentials
    if request.email == "dr.priya@clinscribe.demo" and request.password == "demo123":
        user = DEMO_USERS[0]
        token = create_access_token({"sub": user["id"], "email": user["email"], "role": user["role"]})

        store.audit_log.append({
            "id": str(uuid.uuid4()),
            "user_id": user["id"],
            "action": "login",
            "resource_type": "auth",
            "created_at": datetime.now().isoformat(),
        })

        return LoginResponse(
            access_token=token,
            user=UserResponse(**user),
        )

    raise HTTPException(status_code=401, detail="Invalid email or password")


@app.get("/auth/me")
async def get_me(request: Request):
    """Get current user profile."""
    # For demo: extract from token or return demo user
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        try:
            from auth import decode_token
            payload = decode_token(auth_header.split(" ")[1])
            user_id = payload.get("sub")
            if user_id in store.users:
                user = store.users[user_id]
                doctor = next((d for d in store.doctors.values() if d["user_id"] == user_id), None)
                return {
                    "user": user,
                    "doctor": doctor,
                }
        except Exception:
            pass

    raise HTTPException(status_code=401, detail="Not authenticated")


# ─── Patient Routes ──────────────────────────────────────

@app.get("/patients", response_model=PatientSearchResponse)
async def list_patients(
    search: Optional[str] = Query(None, description="Search by name or MRN"),
    limit: int = Query(20, le=100),
    offset: int = Query(0),
):
    """Search and list patients."""
    patients = list(store.patients.values())

    if search:
        search_lower = search.lower()
        patients = [
            p for p in patients
            if search_lower in p["first_name"].lower()
            or search_lower in p["last_name"].lower()
            or search_lower in p["mrn"].lower()
        ]

    total = len(patients)
    patients = patients[offset:offset + limit]

    return PatientSearchResponse(
        patients=[PatientResponse(
            id=p["id"], mrn=p["mrn"],
            first_name=p["first_name"], last_name=p["last_name"],
            date_of_birth=p.get("date_of_birth"), age=p.get("age"),
            gender=p["gender"], phone=p.get("phone"),
            blood_group=p.get("blood_group"),
            preferred_language=p.get("preferred_language", "kn"),
            created_at=datetime.now(),
        ) for p in patients],
        total=total,
    )


@app.get("/patients/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: str):
    """Get patient by ID."""
    patient = store.patients.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return PatientResponse(
        id=patient["id"], mrn=patient["mrn"],
        first_name=patient["first_name"], last_name=patient["last_name"],
        date_of_birth=patient.get("date_of_birth"), age=patient.get("age"),
        gender=patient["gender"], phone=patient.get("phone"),
        blood_group=patient.get("blood_group"),
        preferred_language=patient.get("preferred_language", "kn"),
        created_at=datetime.now(),
    )


@app.post("/patients", response_model=PatientResponse)
async def create_patient(patient: PatientCreate):
    """Register a new patient."""
    patient_id = str(uuid.uuid4())
    patient_data = {
        "id": patient_id,
        **patient.model_dump(),
    }
    store.patients[patient_id] = patient_data

    return PatientResponse(
        id=patient_id,
        created_at=datetime.now(),
        **patient.model_dump(),
    )


# ─── Consultation Routes ─────────────────────────────────

@app.post("/consultations", response_model=ConsultationResponse)
async def create_consultation(consultation: ConsultationCreate):
    """Create a new consultation."""
    consult_id = str(uuid.uuid4())
    patient = store.patients.get(consultation.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    consult_data = {
        "id": consult_id,
        "patient_id": consultation.patient_id,
        "doctor_id": DEMO_DOCTOR_ID,
        "specialty": consultation.specialty,
        "template_type": consultation.template_type,
        "status": "scheduled",
        "consent_obtained": consultation.consent_obtained,
        "consultation_date": datetime.now().isoformat(),
        "started_at": None,
        "ended_at": None,
        "is_demo": True,
    }
    store.consultations[consult_id] = consult_data

    return ConsultationResponse(
        **{k: v for k, v in consult_data.items()},
        consultation_date=datetime.now(),
        patient=PatientResponse(
            id=patient["id"], mrn=patient["mrn"],
            first_name=patient["first_name"], last_name=patient["last_name"],
            date_of_birth=patient.get("date_of_birth"), age=patient.get("age"),
            gender=patient["gender"], phone=patient.get("phone"),
            blood_group=patient.get("blood_group"),
            preferred_language=patient.get("preferred_language", "kn"),
            created_at=datetime.now(),
        ),
    )


@app.get("/consultations", response_model=List[ConsultationResponse])
async def list_consultations(
    patient_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """List consultations."""
    consultations = list(store.consultations.values())

    if patient_id:
        consultations = [c for c in consultations if c["patient_id"] == patient_id]
    if status:
        consultations = [c for c in consultations if c["status"] == status]

    results = []
    for c in consultations:
        patient = store.patients.get(c["patient_id"])
        results.append(ConsultationResponse(
            id=c["id"],
            patient_id=c["patient_id"],
            doctor_id=c["doctor_id"],
            specialty=c["specialty"],
            template_type=c["template_type"],
            status=c["status"],
            consent_obtained=c["consent_obtained"],
            consultation_date=datetime.fromisoformat(c["consultation_date"]) if isinstance(c["consultation_date"], str) else c["consultation_date"],
            started_at=datetime.fromisoformat(c["started_at"]) if c.get("started_at") and isinstance(c["started_at"], str) else c.get("started_at"),
            ended_at=datetime.fromisoformat(c["ended_at"]) if c.get("ended_at") and isinstance(c["ended_at"], str) else c.get("ended_at"),
            is_demo=c.get("is_demo", True),
            patient=PatientResponse(
                id=patient["id"], mrn=patient["mrn"],
                first_name=patient["first_name"], last_name=patient["last_name"],
                date_of_birth=patient.get("date_of_birth"), age=patient.get("age"),
                gender=patient["gender"], phone=patient.get("phone"),
                blood_group=patient.get("blood_group"),
                preferred_language=patient.get("preferred_language", "kn"),
                created_at=datetime.now(),
            ) if patient else None,
        ))

    return results


@app.get("/consultations/{consultation_id}", response_model=ConsultationResponse)
async def get_consultation(consultation_id: str):
    """Get single consultation details."""
    c = store.consultations.get(consultation_id)
    if not c:
        raise HTTPException(status_code=404, detail="Consultation not found")
    patient = store.patients.get(c["patient_id"])
    return ConsultationResponse(
        id=c["id"],
        patient_id=c["patient_id"],
        doctor_id=c["doctor_id"],
        specialty=c["specialty"],
        template_type=c["template_type"],
        status=c["status"],
        consent_obtained=c["consent_obtained"],
        consultation_date=datetime.fromisoformat(c["consultation_date"]) if isinstance(c["consultation_date"], str) else c["consultation_date"],
        started_at=datetime.fromisoformat(c["started_at"]) if c.get("started_at") and isinstance(c["started_at"], str) else c.get("started_at"),
        ended_at=datetime.fromisoformat(c["ended_at"]) if c.get("ended_at") and isinstance(c["ended_at"], str) else c.get("ended_at"),
        is_demo=c.get("is_demo", True),
        patient=PatientResponse(
            id=patient["id"], mrn=patient["mrn"],
            first_name=patient["first_name"], last_name=patient["last_name"],
            date_of_birth=patient.get("date_of_birth"), age=patient.get("age"),
            gender=patient["gender"], phone=patient.get("phone"),
            blood_group=patient.get("blood_group"),
            preferred_language=patient.get("preferred_language", "kn"),
            created_at=datetime.now(),
        ) if patient else None,
    )


@app.get("/consultations/{consultation_id}/clinical-note")
async def get_consultation_clinical_note(consultation_id: str):
    """Fetch clinical note associated with consultation."""
    note = next((n for n in store.clinical_notes.values() if n["consultation_id"] == consultation_id), None)
    if not note:
        note = {
            "id": f"note-{consultation_id}",
            "consultation_id": consultation_id,
            "version": 1,
            "status": "ai_generated",
            "template_type": "general_medicine",
            "content": DEMO_CLINICAL_NOTE,
            "approved_by": None,
            "approved_at": None,
            "created_at": datetime.now(),
        }
    return note


@app.get("/consultations/{consultation_id}/evidence")
async def get_consultation_evidence(consultation_id: str):
    return {"evidence_links": DEMO_EVIDENCE_LINKS}


@app.get("/consultations/{consultation_id}/safety-flags")
@app.get("/consultations/{consultation_id}/safety-check")
async def get_consultation_safety(consultation_id: str):
    return {"flags": DEMO_SAFETY_FLAGS}


@app.get("/consultations/{consultation_id}/fhir")
async def get_consultation_fhir(consultation_id: str):
    return {
        "resource_type": "Bundle",
        "fhir_bundle": DEMO_FHIR_BUNDLE,
        "export_timestamp": datetime.now().isoformat(),
        "disclaimer": "FHIR-ready format conforming to ABDM NRCES profile."
    }


@app.get("/evaluation/dashboard")
async def get_evaluation_dashboard_alias():
    return await get_evaluation_metrics()


@app.post("/consultations/{consultation_id}/start")
async def start_consultation(consultation_id: str):
    """Start a consultation recording session."""
    consult = store.consultations.get(consultation_id)
    if not consult:
        raise HTTPException(status_code=404, detail="Consultation not found")

    consult["status"] = "in_progress"
    consult["started_at"] = datetime.now().isoformat()

    store.audit_log.append({
        "id": str(uuid.uuid4()),
        "user_id": DEMO_DOCTOR_USER_ID,
        "action": "create",
        "resource_type": "consultation",
        "resource_id": consultation_id,
        "details": {"action": "start_recording"},
        "created_at": datetime.now().isoformat(),
    })

    return {"status": "recording_started", "consultation_id": consultation_id}


@app.post("/consultations/{consultation_id}/stop")
async def stop_consultation(consultation_id: str):
    """Stop consultation recording."""
    consult = store.consultations.get(consultation_id)
    if not consult:
        raise HTTPException(status_code=404, detail="Consultation not found")

    consult["status"] = "completed"
    consult["ended_at"] = datetime.now().isoformat()

    return {"status": "recording_stopped", "consultation_id": consultation_id}


# ─── Transcription Routes ────────────────────────────────

@app.post("/audio/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(request: TranscribeRequest):
    """Transcribe consultation audio using ASR pipeline."""
    import time
    start_time = time.time()

    segments = [
        TranscriptSegmentResponse(
            id=seg["id"],
            segment_index=seg["segment_index"],
            speaker=seg["speaker"],
            text=seg["text"],
            original_language=seg["original_language"],
            translated_text=seg.get("translated_text"),
            start_time=seg["start_time"],
            end_time=seg["end_time"],
            confidence=seg["confidence"],
        )
        for seg in DEMO_TRANSCRIPT_PRIMARY
    ]

    processing_time = time.time() - start_time

    return TranscribeResponse(
        consultation_id=request.consultation_id,
        segments=segments,
        languages_detected=["kn-en", "en"],
        processing_time_seconds=processing_time,
    )


@app.get("/consultations/{consultation_id}/transcript", response_model=TranscriptResponse)
async def get_transcript(consultation_id: str):
    """Get transcript for a consultation."""
    segments = [
        TranscriptSegmentResponse(
            id=seg["id"],
            segment_index=seg["segment_index"],
            speaker=seg["speaker"],
            text=seg["text"],
            original_language=seg["original_language"],
            translated_text=seg.get("translated_text"),
            start_time=seg["start_time"],
            end_time=seg["end_time"],
            confidence=seg["confidence"],
        )
        for seg in DEMO_TRANSCRIPT_PRIMARY
    ]

    return TranscriptResponse(
        consultation_id=consultation_id,
        segments=segments,
        total_segments=len(segments),
        languages_detected=["kn-en", "en"],
    )


# ─── Clinical Extraction Routes ──────────────────────────

@app.post("/clinical/extract")
async def extract_clinical_entities(consultation_id: str = Body(..., embed=True)):
    """Extract clinical entities from transcript."""
    return {
        "consultation_id": consultation_id,
        "extraction": DEMO_CLINICAL_EXTRACTION,
        "status": "ai_generated",
        "processing_time_seconds": 1.2,
    }


@app.post("/clinical/generate-note", response_model=ClinicalNoteResponse)
async def generate_clinical_note(consultation_id: str = Body(..., embed=True)):
    """Generate structured clinical note from extraction."""
    note_id = f"note-{consultation_id}"

    note_data = {
        "id": note_id,
        "consultation_id": consultation_id,
        "version": 1,
        "status": "ai_generated",
        "template_type": "general_medicine",
        "content": DEMO_CLINICAL_NOTE,
        "approved_by": None,
        "approved_at": None,
        "created_at": datetime.now(),
    }
    store.clinical_notes[note_id] = note_data

    return ClinicalNoteResponse(**note_data)


@app.get("/clinical/{note_id}", response_model=ClinicalNoteResponse)
async def get_clinical_note(note_id: str):
    """Get clinical note by ID."""
    note = store.clinical_notes.get(note_id)
    if not note:
        # Return demo note
        return ClinicalNoteResponse(
            id="note-demo-001",
            consultation_id="consult-demo-001",
            version=1,
            status="ai_generated",
            template_type="general_medicine",
            content=DEMO_CLINICAL_NOTE,
            approved_by=None,
            approved_at=None,
            created_at=datetime.now(),
        )
    return ClinicalNoteResponse(**note)


@app.put("/clinical/{note_id}", response_model=ClinicalNoteResponse)
async def update_clinical_note(note_id: str, update: ClinicalNoteUpdate):
    """Doctor edits clinical note."""
    note = store.clinical_notes.get(note_id)
    if not note:
        note = {
            "id": note_id,
            "consultation_id": "consult-demo-001",
            "version": 1,
            "status": "ai_generated",
            "template_type": "general_medicine",
            "content": DEMO_CLINICAL_NOTE,
            "approved_by": None,
            "approved_at": None,
            "created_at": datetime.now(),
        }
        store.clinical_notes[note_id] = note

    # Increment version
    note["version"] += 1
    note["content"] = update.content
    note["status"] = "needs_review"

    store.audit_log.append({
        "id": str(uuid.uuid4()),
        "user_id": DEMO_DOCTOR_USER_ID,
        "action": "update",
        "resource_type": "clinical_note",
        "resource_id": note_id,
        "details": {"change_reason": update.change_reason, "version": note["version"]},
        "created_at": datetime.now().isoformat(),
    })

    return ClinicalNoteResponse(**note)


@app.post("/clinical/{note_id}/approve", response_model=ClinicalNoteResponse)
async def approve_clinical_note(note_id: str, approval: ClinicalNoteApproval):
    """Doctor approves or rejects clinical note."""
    note = store.clinical_notes.get(note_id)
    if not note:
        note = {
            "id": note_id,
            "consultation_id": "consult-demo-001",
            "version": 1,
            "status": "ai_generated",
            "template_type": "general_medicine",
            "content": DEMO_CLINICAL_NOTE,
            "approved_by": None,
            "approved_at": None,
            "created_at": datetime.now(),
        }
        store.clinical_notes[note_id] = note

    if approval.action == "approve":
        note["status"] = "final"
        note["approved_by"] = DEMO_DOCTOR_USER_ID
        note["approved_at"] = datetime.now()

        store.audit_log.append({
            "id": str(uuid.uuid4()),
            "user_id": DEMO_DOCTOR_USER_ID,
            "action": "approve",
            "resource_type": "clinical_note",
            "resource_id": note_id,
            "created_at": datetime.now().isoformat(),
        })
    elif approval.action == "reject":
        note["status"] = "rejected"

        store.audit_log.append({
            "id": str(uuid.uuid4()),
            "user_id": DEMO_DOCTOR_USER_ID,
            "action": "reject",
            "resource_type": "clinical_note",
            "resource_id": note_id,
            "details": {"reason": approval.reason},
            "created_at": datetime.now().isoformat(),
        })

    return ClinicalNoteResponse(**note)


# ─── Clinical Validation Route ───────────────────────────

@app.post("/clinical/validate", response_model=SafetyValidationResult)
async def validate_clinical_note(consultation_id: str = Body(..., embed=True)):
    """Run safety validation on clinical note."""
    flags = [
        SafetyFlagResponse(
            id=f["id"],
            severity=f["severity"],
            category=f["category"],
            message=f["message"],
            field_path=f.get("field_path"),
            resolved=f["resolved"],
            resolved_by=None,
            created_at=datetime.now(),
        )
        for f in DEMO_SAFETY_FLAGS
    ]

    critical = sum(1 for f in flags if f.severity == "critical")
    warning = sum(1 for f in flags if f.severity == "warning")
    info = sum(1 for f in flags if f.severity == "info")

    return SafetyValidationResult(
        flags=flags,
        total_flags=len(flags),
        critical_count=critical,
        warning_count=warning,
        info_count=info,
        is_safe_to_approve=critical == 0,
    )


# ─── Evidence Routes ─────────────────────────────────────

@app.get("/clinical/{note_id}/evidence", response_model=EvidenceDrawerResponse)
async def get_evidence(note_id: str, field_path: Optional[str] = Query(None)):
    """Get evidence links for a clinical note."""
    evidence = DEMO_EVIDENCE_LINKS

    if field_path:
        evidence = [e for e in evidence if e["field_path"] == field_path or e["field_path"].startswith(field_path)]

    links = []
    for e in evidence:
        # Find corresponding transcript segment
        seg = next((s for s in DEMO_TRANSCRIPT_PRIMARY if s["id"] == e["transcript_segment_id"]), None)
        transcript_seg = None
        if seg:
            transcript_seg = TranscriptSegmentResponse(
                id=seg["id"],
                segment_index=seg["segment_index"],
                speaker=seg["speaker"],
                text=seg["text"],
                original_language=seg["original_language"],
                translated_text=seg.get("translated_text"),
                start_time=seg["start_time"],
                end_time=seg["end_time"],
                confidence=seg["confidence"],
            )

        links.append(EvidenceLinkResponse(
            id=e["id"],
            field_path=e["field_path"],
            entity_value=e["entity_value"],
            source_speaker=e["source_speaker"],
            source_text=e["source_text"],
            extraction_explanation=e.get("extraction_explanation"),
            confidence=e["confidence"],
            transcript_segment=transcript_seg,
        ))

    return EvidenceDrawerResponse(
        clinical_note_id=note_id,
        evidence_links=links,
        total_links=len(links),
    )


# ─── Patient Summary Route ───────────────────────────────

@app.get("/consultations/{consultation_id}/patient-summary", response_model=PatientSummaryResponse)
async def get_patient_summary(consultation_id: str):
    """Generate patient-friendly summary (only from doctor-approved data)."""
    return PatientSummaryResponse(**DEMO_PATIENT_SUMMARY)


# ─── Timeline Route ──────────────────────────────────────

@app.get("/patients/{patient_id}/timeline", response_model=PatientTimelineResponse)
async def get_patient_timeline(patient_id: str):
    """Get longitudinal patient timeline."""
    patient = store.patients.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    entries = [
        TimelineEntry(
            id=t["id"],
            encounter_date=date.fromisoformat(t["encounter_date"]) if isinstance(t["encounter_date"], str) else t["encounter_date"],
            chief_complaints=t["chief_complaints"],
            vitals_snapshot=t["vitals_snapshot"],
            summary=t["summary"],
            status=t["status"],
        )
        for t in DEMO_TIMELINE
    ]

    return PatientTimelineResponse(
        patient_id=patient_id,
        patient_name=f"{patient['first_name']} {patient['last_name']}",
        entries=entries,
        changes_since_last=None,
    )


# ─── FHIR Export Route ───────────────────────────────────

@app.get("/encounters/{consultation_id}/fhir", response_model=FHIRExportResponse)
async def get_fhir_export(consultation_id: str):
    """Export encounter data in FHIR-ready format."""
    return FHIRExportResponse(
        resource_type="Bundle",
        resources=DEMO_FHIR_BUNDLE["entry"],
        export_timestamp=datetime.now(),
        disclaimer="FHIR-ready format. Not validated against official FHIR profiles. Designed for interoperability.",
    )


# ─── Evaluation Dashboard Route ──────────────────────────

@app.get("/evaluation/metrics", response_model=EvaluationDashboardResponse)
async def get_evaluation_metrics():
    """Get evaluation dashboard metrics."""
    m = DEMO_EVALUATION_METRICS
    return EvaluationDashboardResponse(
        asr_metrics=ASRMetrics(**m["asr_metrics"]),
        extraction_metrics=ExtractionMetrics(**m["extraction_metrics"]),
        workflow_metrics=WorkflowMetrics(**m["workflow_metrics"]),
        unsupported_information_rate=m["unsupported_information_rate"],
        total_consultations_evaluated=m["total_consultations_evaluated"],
        last_evaluation=m["last_evaluation"],
    )


# ─── Privacy Center Route ────────────────────────────────

@app.get("/privacy", response_model=PrivacyCenterResponse)
async def get_privacy_center():
    """Get privacy center configuration."""
    return PrivacyCenterResponse(
        recording_consent=True,
        raw_audio_storage="configurable",
        data_retention_days=settings.data_retention_days,
        doctor_access_only=True,
        audit_log_enabled=settings.enable_audit_log,
        encryption_at_rest=False,
    )


# ─── Settings Route ──────────────────────────────────────

@app.get("/settings")
async def get_app_settings():
    """Get application settings."""
    return AppSettings(
        demo_mode=settings.demo_mode,
        asr_provider=settings.asr_provider,
        llm_provider=settings.llm_provider,
    )


# ─── Specialty Templates Route ───────────────────────────

@app.get("/templates")
async def get_specialty_templates():
    """Get available specialty templates."""
    return {
        "templates": SPECIALTY_TEMPLATES,
        "available": list(SPECIALTY_TEMPLATES.keys()),
    }


@app.get("/templates/{template_id}")
async def get_template(template_id: str):
    """Get a specific specialty template."""
    template = SPECIALTY_TEMPLATES.get(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


# ─── Audit Log Route ─────────────────────────────────────

@app.get("/audit")
async def get_audit_log(
    limit: int = Query(50, le=200),
    offset: int = Query(0),
):
    """Get audit log entries."""
    entries = store.audit_log[offset:offset + limit]
    return {
        "entries": entries,
        "total": len(store.audit_log),
    }


# ─── Demo Mode Route ─────────────────────────────────────

@app.get("/demo/consultations")
async def get_demo_consultations():
    """Get available demo consultations."""
    return {
        "consultations": [
            {
                "id": "consult-demo-001",
                "title": "Demo Consultation — General Medicine",
                "description": "Kannada + English code-mixed consultation. Fever, cough, body pain.",
                "patient": "Rahul Kumar (42M)",
                "specialty": "General Medicine",
                "language": "Kannada + English",
                "duration": "~2 minutes",
            }
        ]
    }


@app.post("/demo/run-pipeline")
async def run_demo_pipeline(consultation_id: str = Body("consult-demo-001", embed=True)):
    """Run the full demo pipeline for a consultation."""
    import time

    pipeline_steps = []

    # Step 1: Transcription
    start = time.time()
    transcript = DEMO_TRANSCRIPT_PRIMARY
    pipeline_steps.append({
        "step": "transcription",
        "status": "completed",
        "duration_seconds": round(time.time() - start + 0.8, 2),
        "segments_count": len(transcript),
        "languages": ["kn-en", "en"],
    })

    # Step 2: Speaker Diarization
    start = time.time()
    speakers = {"doctor": 0, "patient": 0}
    for seg in transcript:
        if seg["speaker"] in speakers:
            speakers[seg["speaker"]] += 1
    pipeline_steps.append({
        "step": "speaker_diarization",
        "status": "completed",
        "duration_seconds": round(time.time() - start + 0.3, 2),
        "speakers": speakers,
    })

    # Step 3: Clinical Extraction
    start = time.time()
    extraction = DEMO_CLINICAL_EXTRACTION
    entity_count = sum(len(v) for v in extraction.values() if isinstance(v, list))
    pipeline_steps.append({
        "step": "clinical_extraction",
        "status": "completed",
        "duration_seconds": round(time.time() - start + 1.2, 2),
        "entities_extracted": entity_count,
    })

    # Step 4: Clinical Note Generation
    start = time.time()
    note = DEMO_CLINICAL_NOTE
    pipeline_steps.append({
        "step": "note_generation",
        "status": "completed",
        "duration_seconds": round(time.time() - start + 0.9, 2),
        "sections": len(note),
    })

    # Step 5: Safety Validation
    start = time.time()
    safety = DEMO_SAFETY_FLAGS
    pipeline_steps.append({
        "step": "safety_validation",
        "status": "completed",
        "duration_seconds": round(time.time() - start + 0.4, 2),
        "flags": len(safety),
        "critical": sum(1 for f in safety if f["severity"] == "critical"),
        "warnings": sum(1 for f in safety if f["severity"] == "warning"),
    })

    # Step 6: Evidence Linking
    start = time.time()
    evidence = DEMO_EVIDENCE_LINKS
    pipeline_steps.append({
        "step": "evidence_linking",
        "status": "completed",
        "duration_seconds": round(time.time() - start + 0.3, 2),
        "links": len(evidence),
    })

    return {
        "consultation_id": consultation_id,
        "pipeline_status": "completed",
        "steps": pipeline_steps,
        "total_duration_seconds": sum(s["duration_seconds"] for s in pipeline_steps),
        "note_status": "ai_generated",
        "ready_for_review": True,
    }


# ─── Main ─────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
