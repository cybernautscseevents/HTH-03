"""
ClinScribe AI — Pydantic Schemas
Request/Response models for API endpoints.
Every AI output carries source references, confidence, and status.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


# ─── Enums ────────────────────────────────────────────────

class UserRole(str, Enum):
    DOCTOR = "doctor"
    NURSE = "nurse"
    ADMIN = "admin"
    STAFF = "staff"


class ConsultationStatusEnum(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ClinicalStatusEnum(str, Enum):
    AI_GENERATED = "ai_generated"
    NEEDS_REVIEW = "needs_review"
    VERIFIED = "verified"
    REJECTED = "rejected"
    FINAL = "final"


class SpeakerRoleEnum(str, Enum):
    DOCTOR = "doctor"
    PATIENT = "patient"
    OTHER = "other"
    UNKNOWN = "unknown"


class SymptomPresenceEnum(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    UNKNOWN = "unknown"


class SafetySeverityEnum(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


# ─── Auth ─────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class DoctorResponse(BaseModel):
    id: str
    user_id: str
    registration_number: Optional[str]
    specialty: str
    department: Optional[str]
    preferred_language: str
    preferred_template: str
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True


# ─── Patient ─────────────────────────────────────────────

class PatientCreate(BaseModel):
    mrn: str
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    age: Optional[int] = None
    gender: str = "unknown"
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None
    preferred_language: str = "kn"


class PatientResponse(BaseModel):
    id: str
    mrn: str
    first_name: str
    last_name: str
    date_of_birth: Optional[date]
    age: Optional[int]
    gender: str
    phone: Optional[str]
    blood_group: Optional[str]
    preferred_language: str
    created_at: datetime

    class Config:
        from_attributes = True


class PatientSearchResponse(BaseModel):
    patients: List[PatientResponse]
    total: int


# ─── Consultation ─────────────────────────────────────────

class ConsultationCreate(BaseModel):
    patient_id: str
    specialty: str = "General Medicine"
    template_type: str = "general_medicine"
    consent_obtained: bool = False


class ConsultationResponse(BaseModel):
    id: str
    patient_id: str
    doctor_id: str
    specialty: str
    template_type: str
    status: ConsultationStatusEnum
    consent_obtained: bool
    consultation_date: datetime
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    is_demo: bool
    patient: Optional[PatientResponse] = None

    class Config:
        from_attributes = True


# ─── Transcript ───────────────────────────────────────────

class TranscriptSegmentResponse(BaseModel):
    id: str
    segment_index: int
    speaker: SpeakerRoleEnum
    text: str
    original_language: str
    translated_text: Optional[str]
    start_time: float
    end_time: float
    confidence: float

    class Config:
        from_attributes = True


class TranscriptResponse(BaseModel):
    consultation_id: str
    segments: List[TranscriptSegmentResponse]
    total_segments: int
    languages_detected: List[str]


# ─── Clinical Entity ─────────────────────────────────────

class ClinicalEntityValue(BaseModel):
    """Individual extracted clinical entity with provenance."""
    value: str
    presence: SymptomPresenceEnum = SymptomPresenceEnum.PRESENT
    confidence: float = 0.0
    source_segment_ids: List[str] = []
    status: ClinicalStatusEnum = ClinicalStatusEnum.AI_GENERATED
    attributes: Dict[str, Any] = {}


class ClinicalExtractionResult(BaseModel):
    """Full clinical extraction output from AI pipeline."""
    chief_complaints: List[ClinicalEntityValue] = []
    symptoms: List[ClinicalEntityValue] = []
    negative_findings: List[ClinicalEntityValue] = []
    duration: List[ClinicalEntityValue] = []
    medications: List[ClinicalEntityValue] = []
    allergies: List[ClinicalEntityValue] = []
    vitals: List[ClinicalEntityValue] = []
    examination_findings: List[ClinicalEntityValue] = []
    investigations: List[ClinicalEntityValue] = []
    past_medical_history: List[ClinicalEntityValue] = []
    family_history: List[ClinicalEntityValue] = []
    social_history: List[ClinicalEntityValue] = []
    assessment: List[ClinicalEntityValue] = []
    plan: List[ClinicalEntityValue] = []
    follow_up: List[ClinicalEntityValue] = []
    uncertainties: List[ClinicalEntityValue] = []


# ─── Clinical Note ────────────────────────────────────────

class ClinicalNoteSection(BaseModel):
    title: str
    content: str
    entities: List[ClinicalEntityValue] = []
    status: ClinicalStatusEnum = ClinicalStatusEnum.AI_GENERATED


class ClinicalNoteContent(BaseModel):
    """Structured clinical note content."""
    patient_info: Dict[str, Any] = {}
    chief_complaint: ClinicalNoteSection
    history_of_present_illness: ClinicalNoteSection
    associated_symptoms: ClinicalNoteSection
    negative_findings: ClinicalNoteSection
    past_medical_history: ClinicalNoteSection
    medication_history: ClinicalNoteSection
    allergies: ClinicalNoteSection
    vitals: ClinicalNoteSection
    examination: ClinicalNoteSection
    investigations: ClinicalNoteSection
    assessment: ClinicalNoteSection
    plan: ClinicalNoteSection
    follow_up: ClinicalNoteSection


class ClinicalNoteResponse(BaseModel):
    id: str
    consultation_id: str
    version: int
    status: ClinicalStatusEnum
    template_type: str
    content: Dict[str, Any]
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ClinicalNoteUpdate(BaseModel):
    """Doctor's edits to clinical note."""
    content: Dict[str, Any]
    change_reason: Optional[str] = None


class ClinicalNoteApproval(BaseModel):
    action: str  # "approve" or "reject"
    reason: Optional[str] = None


# ─── Evidence ─────────────────────────────────────────────

class EvidenceLinkResponse(BaseModel):
    id: str
    field_path: str
    entity_value: str
    source_speaker: SpeakerRoleEnum
    source_text: str
    extraction_explanation: Optional[str]
    confidence: float
    transcript_segment: Optional[TranscriptSegmentResponse] = None

    class Config:
        from_attributes = True


class EvidenceDrawerResponse(BaseModel):
    clinical_note_id: str
    evidence_links: List[EvidenceLinkResponse]
    total_links: int


# ─── Safety ───────────────────────────────────────────────

class SafetyFlagResponse(BaseModel):
    id: str
    severity: SafetySeverityEnum
    category: str
    message: str
    field_path: Optional[str]
    resolved: bool
    resolved_by: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class SafetyValidationResult(BaseModel):
    flags: List[SafetyFlagResponse]
    total_flags: int
    critical_count: int
    warning_count: int
    info_count: int
    is_safe_to_approve: bool


# ─── Patient Summary ─────────────────────────────────────

class PatientSummaryResponse(BaseModel):
    consultation_id: str
    patient_name: str
    visit_date: str
    what_you_told_the_doctor: List[str]
    doctors_instructions: List[str]
    medicines: List[str]
    tests: List[str]
    follow_up: str
    language: str
    disclaimer: str = "This summary is for your reference. Follow your doctor's verbal instructions."


# ─── Timeline ─────────────────────────────────────────────

class TimelineEntry(BaseModel):
    id: str
    encounter_date: date
    chief_complaints: List[str]
    vitals_snapshot: Dict[str, Any]
    summary: Dict[str, Any]
    status: ClinicalStatusEnum

    class Config:
        from_attributes = True


class PatientTimelineResponse(BaseModel):
    patient_id: str
    patient_name: str
    entries: List[TimelineEntry]
    changes_since_last: Optional[Dict[str, Any]] = None


# ─── FHIR ─────────────────────────────────────────────────

class FHIRExportResponse(BaseModel):
    """FHIR-ready JSON export."""
    resource_type: str
    resources: List[Dict[str, Any]]
    export_timestamp: datetime
    disclaimer: str = "FHIR-ready format. Not validated against official FHIR profiles."


# ─── Evaluation ───────────────────────────────────────────

class ASRMetrics(BaseModel):
    word_error_rate: Optional[float] = None
    character_error_rate: Optional[float] = None
    samples_evaluated: int = 0
    status: str = "Not yet measured"


class ExtractionMetrics(BaseModel):
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    samples_evaluated: int = 0
    status: str = "Not yet measured"


class WorkflowMetrics(BaseModel):
    avg_documentation_time_seconds: Optional[float] = None
    avg_doctor_correction_time_seconds: Optional[float] = None
    correction_rate: Optional[float] = None
    documentation_time_saved_pct: Optional[float] = None
    status: str = "Not yet measured"


class EvaluationDashboardResponse(BaseModel):
    asr_metrics: ASRMetrics
    extraction_metrics: ExtractionMetrics
    workflow_metrics: WorkflowMetrics
    unsupported_information_rate: Optional[float] = None
    total_consultations_evaluated: int = 0
    last_evaluation: Optional[datetime] = None


# ─── Privacy ──────────────────────────────────────────────

class PrivacyCenterResponse(BaseModel):
    recording_consent: bool = True
    raw_audio_storage: str = "configurable"
    data_retention_days: int = 90
    doctor_access_only: bool = True
    audit_log_enabled: bool = True
    encryption_at_rest: bool = False
    last_audit: Optional[datetime] = None


# ─── Audio Transcription ─────────────────────────────────

class TranscribeRequest(BaseModel):
    consultation_id: str
    language: str = "kn"
    use_demo: bool = False


class TranscribeResponse(BaseModel):
    consultation_id: str
    segments: List[TranscriptSegmentResponse]
    languages_detected: List[str]
    processing_time_seconds: float


# ─── Settings ─────────────────────────────────────────────

class AppSettings(BaseModel):
    demo_mode: bool = True
    asr_provider: str = "demo"
    llm_provider: str = "demo"
    default_language: str = "kn-en"
    available_specialties: List[str] = [
        "General Medicine", "Pediatrics", "Orthopedics",
        "ENT", "Dermatology", "Gynecology", "Cardiology"
    ]
    available_languages: List[str] = [
        "kn-en", "hi-en", "ta-en", "te-en", "ml-en"
    ]
