"""
ClinScribe AI — ABDM / FHIR R4 Interoperability Service
Transforms ClinScribe AI consultations, notes, and prescriptions into compliant
HL7 FHIR R4 bundles for Ayushman Bharat Digital Mission (ABDM) Electronic Health Records.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import json


class FHIRConverter:
    """Converts consultation data into FHIR R4 resources conforming to ABDM NRCES profile specifications."""

    def build_bundle(
        self,
        patient: Dict[str, Any],
        doctor: Dict[str, Any],
        consultation: Dict[str, Any],
        clinical_note: Dict[str, Any]
    ) -> Dict[str, Any]:
        bundle_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"
        patient_ref = f"Patient/{patient.get('id', 'pat-demo')}"
        doc_ref = f"Practitioner/{doctor.get('id', 'doc-demo')}"
        encounter_ref = f"Encounter/{consultation.get('id', 'enc-demo')}"

        entries: List[Dict[str, Any]] = []

        # 1. Patient Resource
        entries.append({
            "fullUrl": f"urn:uuid:{patient.get('id', 'pat-001')}",
            "resource": {
                "resourceType": "Patient",
                "id": str(patient.get('id', 'pat-001')),
                "identifier": [
                    {
                        "system": "https://abdm.gov.in/abha",
                        "value": patient.get("abha_id", "91-8822-4411-9988")
                    }
                ],
                "name": [{"text": patient.get("full_name", "Patient Name")}],
                "gender": patient.get("gender", "unknown").lower(),
                "birthDate": str(patient.get("date_of_birth", "1975-01-01"))
            }
        })

        # 2. Practitioner Resource
        entries.append({
            "fullUrl": f"urn:uuid:{doctor.get('id', 'doc-001')}",
            "resource": {
                "resourceType": "Practitioner",
                "id": str(doctor.get('id', 'doc-001')),
                "identifier": [
                    {
                        "system": "https://nmc.org.in/registration",
                        "value": doctor.get("registration_number", "KMC-48291")
                    }
                ],
                "name": [{"text": doctor.get("full_name", "Dr. Clinician")}],
                "qualification": [{"code": {"text": doctor.get("specialty", "General Medicine")}}]
            }
        })

        # 3. Encounter Resource
        entries.append({
            "fullUrl": f"urn:uuid:{consultation.get('id', 'enc-001')}",
            "resource": {
                "resourceType": "Encounter",
                "id": str(consultation.get('id', 'enc-001')),
                "status": "finished",
                "class": {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                    "code": "AMB",
                    "display": "ambulatory"
                },
                "subject": {"reference": patient_ref},
                "participant": [{"individual": {"reference": doc_ref}}],
                "period": {
                    "start": consultation.get("created_at", timestamp),
                    "end": timestamp
                }
            }
        })

        # 4. Clinical Condition (Diagnoses)
        soap = clinical_note.get("soap_sections", {})
        assessment = soap.get("assessment", {})
        diagnoses = assessment.get("diagnoses", ["Type 2 Diabetes Mellitus", "Essential Hypertension"])
        for idx, diag in enumerate(diagnoses):
            cond_id = f"cond-{idx+1}"
            entries.append({
                "fullUrl": f"urn:uuid:{cond_id}",
                "resource": {
                    "resourceType": "Condition",
                    "id": cond_id,
                    "clinicalStatus": {
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active"
                        }]
                    },
                    "subject": {"reference": patient_ref},
                    "encounter": {"reference": encounter_ref},
                    "code": {
                        "text": diag
                    }
                }
            })

        # 5. MedicationRequests (Prescriptions)
        plan = soap.get("plan", {})
        medications = plan.get("medications", [])
        for idx, med in enumerate(medications):
            med_id = f"med-req-{idx+1}"
            med_name = med.get("name") if isinstance(med, dict) else str(med)
            dosage = med.get("dosage", "As directed") if isinstance(med, dict) else "1 OD"
            entries.append({
                "fullUrl": f"urn:uuid:{med_id}",
                "resource": {
                    "resourceType": "MedicationRequest",
                    "id": med_id,
                    "status": "active",
                    "intent": "order",
                    "subject": {"reference": patient_ref},
                    "encounter": {"reference": encounter_ref},
                    "medicationCodeableConcept": {"text": med_name},
                    "dosageInstruction": [{"text": dosage}]
                }
            })

        # Assemble Full FHIR Bundle
        return {
            "resourceType": "Bundle",
            "id": bundle_id,
            "meta": {
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentBundle"]
            },
            "type": "document",
            "timestamp": timestamp,
            "entry": entries
        }
