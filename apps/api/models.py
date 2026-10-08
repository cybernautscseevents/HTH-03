"""
ClinScribe AI — Database Models
Normalized PostgreSQL schema for clinical documentation system.
Every clinical note has version history. Audit logging is built-in.
"""

import uuid
from datetime import datetime, date
from enum import Enum as PyEnum
from typing import Optional, List

from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Date, Text,
    ForeignKey, Enum, JSON, Index, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


# ─── Enums ────────────────────────────────────────────────

class UserRole(str, PyEnum):
    DOCTOR = "doctor"
    NURSE = "nurse"
    ADMIN = "admin"
    STAFF = "staff"


class ConsultationStatus(str, PyEnum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RecordingStatus(str, PyEnum):
    NOT_STARTED = "not_started"
    RECORDING = "recording"
    PAUSED = "paused"
    STOPPED = "stopped"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class SpeakerRole(str, PyEnum):
    DOCTOR = "doctor"
    PATIENT = "patient"
    OTHER = "other"
    UNKNOWN = "unknown"


class ClinicalStatus(str, PyEnum):
    AI_GENERATED = "ai_generated"
    NEEDS_REVIEW = "needs_review"
    VERIFIED = "verified"
    REJECTED = "rejected"
    FINAL = "final"


class SymptomPresence(str, PyEnum):
    PRESENT = "present"
    ABSENT = "absent"
    UNKNOWN = "unknown"


class SafetyFlagSeverity(str, PyEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AuditAction(str, PyEnum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    CONSENT = "consent"


# ─── Users & Auth ─────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.DOCTOR)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    doctor_profile = relationship("Doctor", back_populates="user", uselist=False)


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    registration_number: Mapped[str] = mapped_column(String(100), nullable=True)
    specialty: Mapped[str] = mapped_column(String(100), nullable=False, default="General Medicine")
    department: Mapped[str] = mapped_column(String(100), nullable=True)
    hospital_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("hospitals.id"), nullable=True)
    preferred_language: Mapped[str] = mapped_column(String(50), default="en")
    preferred_template: Mapped[str] = mapped_column(String(100), default="general_medicine")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="doctor_profile")
    consultations = relationship("Consultation", back_populates="doctor")


# ─── Hospital ─────────────────────────────────────────────

class Hospital(Base):
    __tablename__ = "hospitals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hospital_id: Mapped[str] = mapped_column(String(36), ForeignKey("hospitals.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)


# ─── Patients ─────────────────────────────────────────────

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mrn: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=False, default="unknown")
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    blood_group: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    preferred_language: Mapped[str] = mapped_column(String(50), default="kn")
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    consultations = relationship("Consultation", back_populates="patient")
    timeline_entries = relationship("PatientTimeline", back_populates="patient")


# ─── Consultations ────────────────────────────────────────

class Consultation(Base):
    __tablename__ = "consultations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    doctor_id: Mapped[str] = mapped_column(String(36), ForeignKey("doctors.id"), nullable=False, index=True)
    specialty: Mapped[str] = mapped_column(String(100), default="General Medicine")
    template_type: Mapped[str] = mapped_column(String(100), default="general_medicine")
    status: Mapped[str] = mapped_column(Enum(ConsultationStatus), default=ConsultationStatus.SCHEDULED)
    consent_obtained: Mapped[bool] = mapped_column(Boolean, default=False)
    consultation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="consultations")
    doctor = relationship("Doctor", back_populates="consultations")
    audio_session = relationship("AudioSession", back_populates="consultation", uselist=False)
    transcript_segments = relationship("TranscriptSegment", back_populates="consultation", order_by="TranscriptSegment.start_time")
    clinical_entities = relationship("ClinicalEntity", back_populates="consultation")
    clinical_notes = relationship("ClinicalNote", back_populates="consultation")
    safety_flags = relationship("SafetyFlag", back_populates="consultation")


# ─── Audio ────────────────────────────────────────────────

class AudioSession(Base):
    __tablename__ = "audio_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    consultation_id: Mapped[str] = mapped_column(String(36), ForeignKey("consultations.id"), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(Enum(RecordingStatus), default=RecordingStatus.NOT_STARTED)
    duration_seconds: Mapped[float] = mapped_column(Float, default=0.0)
    audio_file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    sample_rate: Mapped[int] = mapped_column(Integer, default=16000)
    channels: Mapped[int] = mapped_column(Integer, default=1)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    consultation = relationship("Consultation", back_populates="audio_session")


# ─── Transcript ───────────────────────────────────────────

class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    consultation_id: Mapped[str] = mapped_column(String(36), ForeignKey("consultations.id"), nullable=False, index=True)
    segment_index: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker: Mapped[str] = mapped_column(Enum(SpeakerRole), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    original_language: Mapped[str] = mapped_column(String(50), default="kn-en")
    translated_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_time: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    end_time: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    consultation = relationship("Consultation", back_populates="transcript_segments")
    evidence_links = relationship("EvidenceLink", back_populates="transcript_segment")


# ─── Clinical Entities ────────────────────────────────────

class ClinicalEntity(Base):
    __tablename__ = "clinical_entities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    consultation_id: Mapped[str] = mapped_column(String(36), ForeignKey("consultations.id"), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)  # symptom, medication, vital, etc.
    value: Mapped[str] = mapped_column(Text, nullable=False)
    presence: Mapped[str] = mapped_column(Enum(SymptomPresence), default=SymptomPresence.PRESENT)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    attributes: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)  # duration, severity, frequency, etc.
    source_segment_ids: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(Enum(ClinicalStatus), default=ClinicalStatus.AI_GENERATED)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    consultation = relationship("Consultation", back_populates="clinical_entities")


# ─── Clinical Notes ───────────────────────────────────────

class ClinicalNote(Base):
    __tablename__ = "clinical_notes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    consultation_id: Mapped[str] = mapped_column(String(36), ForeignKey("consultations.id"), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(Enum(ClinicalStatus), default=ClinicalStatus.AI_GENERATED)
    template_type: Mapped[str] = mapped_column(String(100), default="general_medicine")
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)
    approved_by: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    consultation = relationship("Consultation", back_populates="clinical_notes")
    versions = relationship("ClinicalNoteVersion", back_populates="clinical_note")
    evidence_links = relationship("EvidenceLink", back_populates="clinical_note")


class ClinicalNoteVersion(Base):
    __tablename__ = "clinical_note_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clinical_note_id: Mapped[str] = mapped_column(String(36), ForeignKey("clinical_notes.id"), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)
    changed_by: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    change_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    clinical_note = relationship("ClinicalNote", back_populates="versions")


# ─── Evidence Links ───────────────────────────────────────

class EvidenceLink(Base):
    __tablename__ = "evidence_links"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clinical_note_id: Mapped[str] = mapped_column(String(36), ForeignKey("clinical_notes.id"), nullable=False, index=True)
    field_path: Mapped[str] = mapped_column(String(255), nullable=False)
    entity_value: Mapped[str] = mapped_column(Text, nullable=False)
    transcript_segment_id: Mapped[str] = mapped_column(String(36), ForeignKey("transcript_segments.id"), nullable=False)
    source_speaker: Mapped[str] = mapped_column(Enum(SpeakerRole), nullable=False)
    source_text: Mapped[str] = mapped_column(Text, nullable=False)
    extraction_explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    clinical_note = relationship("ClinicalNote", back_populates="evidence_links")
    transcript_segment = relationship("TranscriptSegment", back_populates="evidence_links")


# ─── Safety ───────────────────────────────────────────────

class SafetyFlag(Base):
    __tablename__ = "safety_flags"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    consultation_id: Mapped[str] = mapped_column(String(36), ForeignKey("consultations.id"), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(Enum(SafetyFlagSeverity), default=SafetyFlagSeverity.WARNING)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    field_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    resolved_by: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    consultation = relationship("Consultation", back_populates="safety_flags")


# ─── Medications ──────────────────────────────────────────

class Medication(Base):
    __tablename__ = "medications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    consultation_id: Mapped[str] = mapped_column(String(36), ForeignKey("consultations.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    dosage: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    frequency: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    duration: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    route: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(Enum(ClinicalStatus), default=ClinicalStatus.AI_GENERATED)
    source_segment_ids: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ─── Observations / Vitals ────────────────────────────────

class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    consultation_id: Mapped[str] = mapped_column(String(36), ForeignKey("consultations.id"), nullable=False, index=True)
    observation_type: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(Enum(ClinicalStatus), default=ClinicalStatus.AI_GENERATED)
    source_segment_ids: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ─── Investigations ───────────────────────────────────────

class Investigation(Base):
    __tablename__ = "investigations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    consultation_id: Mapped[str] = mapped_column(String(36), ForeignKey("consultations.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ordered")
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    clinical_status: Mapped[str] = mapped_column(Enum(ClinicalStatus), default=ClinicalStatus.AI_GENERATED)
    source_segment_ids: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ─── Patient Timeline ────────────────────────────────────

class PatientTimeline(Base):
    __tablename__ = "patient_timelines"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    consultation_id: Mapped[str] = mapped_column(String(36), ForeignKey("consultations.id"), nullable=False)
    encounter_date: Mapped[date] = mapped_column(Date, nullable=False)
    summary: Mapped[dict] = mapped_column(JSONB, nullable=False)
    chief_complaints: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    vitals_snapshot: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(Enum(ClinicalStatus), default=ClinicalStatus.FINAL)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="timeline_entries")


# ─── Consent ──────────────────────────────────────────────

class ConsentRecord(Base):
    __tablename__ = "consent_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    consultation_id: Mapped[str] = mapped_column(String(36), ForeignKey("consultations.id"), nullable=False)
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False)
    consent_type: Mapped[str] = mapped_column(String(100), default="recording")
    consented: Mapped[bool] = mapped_column(Boolean, default=False)
    consented_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    withdrawn_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ─── Audit Log ────────────────────────────────────────────

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(Enum(AuditAction), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    details: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ─── Evaluation ───────────────────────────────────────────

class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    run_type: Mapped[str] = mapped_column(String(100), nullable=False)
    dataset: Mapped[str] = mapped_column(String(255), nullable=False)
    metrics: Mapped[dict] = mapped_column(JSONB, nullable=False)
    config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
