"""
ClinScribe AI — Synthetic Demo Data
Pre-built consultation scenarios for reliable hackathon demonstration.
All data is synthetic. No real patient information is used.
"""

import uuid
from datetime import datetime, date, timedelta


def generate_id() -> str:
    return str(uuid.uuid4())


# ─── Demo Users ───────────────────────────────────────────

DEMO_DOCTOR_ID = "doc-demo-001"
DEMO_DOCTOR_USER_ID = "user-demo-001"

DEMO_USERS = [
    {
        "id": DEMO_DOCTOR_USER_ID,
        "email": "dr.priya@clinscribe.demo",
        "full_name": "Dr. Priya Sharma",
        "role": "doctor",
        "is_active": True,
    }
]

DEMO_DOCTORS = [
    {
        "id": DEMO_DOCTOR_ID,
        "user_id": DEMO_DOCTOR_USER_ID,
        "registration_number": "KMC-2019-45678",
        "specialty": "General Medicine",
        "department": "OPD",
        "preferred_language": "kn-en",
        "preferred_template": "general_medicine",
    }
]

# ─── Demo Patients ────────────────────────────────────────

DEMO_PATIENTS = [
    {
        "id": "pat-demo-001",
        "mrn": "MRN-2026-0001",
        "first_name": "Rahul",
        "last_name": "Kumar",
        "date_of_birth": "1984-05-15",
        "age": 42,
        "gender": "male",
        "phone": "+91-98765-43210",
        "blood_group": "B+",
        "preferred_language": "kn",
    },
    {
        "id": "pat-demo-002",
        "mrn": "MRN-2026-0002",
        "first_name": "Lakshmi",
        "last_name": "Devi",
        "date_of_birth": "1990-11-22",
        "age": 35,
        "gender": "female",
        "phone": "+91-87654-32100",
        "blood_group": "O+",
        "preferred_language": "kn",
    },
    {
        "id": "pat-demo-003",
        "mrn": "MRN-2026-0003",
        "first_name": "Arjun",
        "last_name": "Reddy",
        "date_of_birth": "1975-03-08",
        "age": 51,
        "gender": "male",
        "phone": "+91-76543-21000",
        "blood_group": "A+",
        "preferred_language": "te",
    },
    {
        "id": "pat-demo-004",
        "mrn": "MRN-2026-0004",
        "first_name": "Meera",
        "last_name": "Nair",
        "date_of_birth": "2020-07-14",
        "age": 6,
        "gender": "female",
        "phone": "+91-65432-10987",
        "blood_group": "AB+",
        "preferred_language": "ml",
    },
    {
        "id": "pat-demo-005",
        "mrn": "MRN-2026-0005",
        "first_name": "Vikram",
        "last_name": "Singh",
        "date_of_birth": "1968-12-01",
        "age": 57,
        "gender": "male",
        "phone": "+91-54321-09876",
        "blood_group": "B-",
        "preferred_language": "hi",
    },
]

# ─── Primary Demo Consultation: Kannada + English ─────────

DEMO_CONSULTATION_PRIMARY = {
    "id": "consult-demo-001",
    "patient_id": "pat-demo-001",
    "doctor_id": DEMO_DOCTOR_ID,
    "specialty": "General Medicine",
    "template_type": "general_medicine",
    "status": "completed",
    "consent_obtained": True,
    "is_demo": True,
}

# The primary demo transcript (Kannada + English code-mixed)
DEMO_TRANSCRIPT_PRIMARY = [
    {
        "id": "seg-001",
        "segment_index": 0,
        "speaker": "doctor",
        "text": "Namaskara, Rahul. Hēgiddīra? Yāvudādarū problem ide?",
        "translated_text": "Hello, Rahul. How are you? Is there any problem?",
        "original_language": "kn-en",
        "start_time": 0.0,
        "end_time": 4.2,
        "confidence": 0.94,
    },
    {
        "id": "seg-002",
        "segment_index": 1,
        "speaker": "patient",
        "text": "Doctor, nange three days inda fever ide.",
        "translated_text": "Doctor, I have had fever for three days.",
        "original_language": "kn-en",
        "start_time": 4.5,
        "end_time": 7.8,
        "confidence": 0.96,
    },
    {
        "id": "seg-003",
        "segment_index": 2,
        "speaker": "doctor",
        "text": "Fever yavaga inda ide? Exact yavāga start āytu?",
        "translated_text": "Since when do you have fever? When exactly did it start?",
        "original_language": "kn-en",
        "start_time": 8.0,
        "end_time": 11.5,
        "confidence": 0.93,
    },
    {
        "id": "seg-004",
        "segment_index": 3,
        "speaker": "patient",
        "text": "Monday night inda start āytu, swalpa mild ide ansutte initially, āmēle Tuesday inda jaasti āytu.",
        "translated_text": "It started from Monday night, initially it seemed mild, then from Tuesday it increased.",
        "original_language": "kn-en",
        "start_time": 12.0,
        "end_time": 18.2,
        "confidence": 0.91,
    },
    {
        "id": "seg-005",
        "segment_index": 4,
        "speaker": "doctor",
        "text": "Temperature check māḍidra? Highest temperature ēṣṭu itta?",
        "translated_text": "Did you check the temperature? What was the highest temperature?",
        "original_language": "kn-en",
        "start_time": 18.5,
        "end_time": 22.0,
        "confidence": 0.92,
    },
    {
        "id": "seg-006",
        "segment_index": 5,
        "speaker": "patient",
        "text": "Hūdu doctor, 101 point 5 itta yesterday.",
        "translated_text": "Yes doctor, it was 101.5 yesterday.",
        "original_language": "kn-en",
        "start_time": 22.3,
        "end_time": 25.5,
        "confidence": 0.95,
    },
    {
        "id": "seg-007",
        "segment_index": 6,
        "speaker": "doctor",
        "text": "Cough ideya?",
        "translated_text": "Do you have cough?",
        "original_language": "kn-en",
        "start_time": 26.0,
        "end_time": 27.5,
        "confidence": 0.97,
    },
    {
        "id": "seg-008",
        "segment_index": 7,
        "speaker": "patient",
        "text": "Yes doctor, cough ide. Night time alli jaasti agutte. Dry cough tarah ide.",
        "translated_text": "Yes doctor, I have cough. It gets worse at night. It seems like a dry cough.",
        "original_language": "kn-en",
        "start_time": 27.8,
        "end_time": 33.0,
        "confidence": 0.94,
    },
    {
        "id": "seg-009",
        "segment_index": 8,
        "speaker": "doctor",
        "text": "Cold ideya? Running nose?",
        "translated_text": "Do you have cold? Running nose?",
        "original_language": "kn-en",
        "start_time": 33.5,
        "end_time": 35.5,
        "confidence": 0.96,
    },
    {
        "id": "seg-010",
        "segment_index": 9,
        "speaker": "patient",
        "text": "Swalpa ide doctor, but adhu jaasti illa.",
        "translated_text": "A little bit doctor, but not too much.",
        "original_language": "kn-en",
        "start_time": 36.0,
        "end_time": 39.0,
        "confidence": 0.93,
    },
    {
        "id": "seg-011",
        "segment_index": 10,
        "speaker": "doctor",
        "text": "Chest pain ideya? Breathlessness?",
        "translated_text": "Do you have chest pain? Breathlessness?",
        "original_language": "kn-en",
        "start_time": 39.5,
        "end_time": 42.0,
        "confidence": 0.97,
    },
    {
        "id": "seg-012",
        "segment_index": 11,
        "speaker": "patient",
        "text": "Illa doctor, chest pain illa. Breathlessness ū illa.",
        "translated_text": "No doctor, no chest pain. No breathlessness either.",
        "original_language": "kn-en",
        "start_time": 42.3,
        "end_time": 46.0,
        "confidence": 0.96,
    },
    {
        "id": "seg-013",
        "segment_index": 12,
        "speaker": "doctor",
        "text": "Vomiting? Loose stools?",
        "translated_text": "Vomiting? Loose stools?",
        "original_language": "kn-en",
        "start_time": 46.5,
        "end_time": 48.5,
        "confidence": 0.97,
    },
    {
        "id": "seg-014",
        "segment_index": 13,
        "speaker": "patient",
        "text": "Illa doctor, vomiting illa. Stools normal ide.",
        "translated_text": "No doctor, no vomiting. Stools are normal.",
        "original_language": "kn-en",
        "start_time": 49.0,
        "end_time": 52.5,
        "confidence": 0.95,
    },
    {
        "id": "seg-015",
        "segment_index": 14,
        "speaker": "doctor",
        "text": "Body pain ideya? Head pain?",
        "translated_text": "Do you have body pain? Headache?",
        "original_language": "kn-en",
        "start_time": 53.0,
        "end_time": 55.5,
        "confidence": 0.96,
    },
    {
        "id": "seg-016",
        "segment_index": 15,
        "speaker": "patient",
        "text": "Hūdu, body pain ide. Head pain ū swalpa ide.",
        "translated_text": "Yes, I have body pain. A little headache too.",
        "original_language": "kn-en",
        "start_time": 56.0,
        "end_time": 60.0,
        "confidence": 0.93,
    },
    {
        "id": "seg-017",
        "segment_index": 16,
        "speaker": "doctor",
        "text": "Allergy ēnādarū ideya? Any medication allergy?",
        "translated_text": "Do you have any allergies? Any medication allergy?",
        "original_language": "kn-en",
        "start_time": 60.5,
        "end_time": 64.0,
        "confidence": 0.94,
    },
    {
        "id": "seg-018",
        "segment_index": 17,
        "speaker": "patient",
        "text": "Illa doctor, yāvudē allergy illa nange.",
        "translated_text": "No doctor, I don't have any allergies.",
        "original_language": "kn-en",
        "start_time": 64.5,
        "end_time": 67.5,
        "confidence": 0.95,
    },
    {
        "id": "seg-019",
        "segment_index": 18,
        "speaker": "doctor",
        "text": "Previous ēnādarū medical history ideya? Diabetes? BP?",
        "translated_text": "Do you have any previous medical history? Diabetes? BP?",
        "original_language": "kn-en",
        "start_time": 68.0,
        "end_time": 72.0,
        "confidence": 0.93,
    },
    {
        "id": "seg-020",
        "segment_index": 19,
        "speaker": "patient",
        "text": "BP swalpa high ide anta last year hēḷidru. Tablet tagonttiddēne. Amlodipine 5 mg.",
        "translated_text": "They told me last year that BP is slightly high. I am taking a tablet. Amlodipine 5 mg.",
        "original_language": "kn-en",
        "start_time": 72.5,
        "end_time": 79.0,
        "confidence": 0.91,
    },
    {
        "id": "seg-021",
        "segment_index": 20,
        "speaker": "doctor",
        "text": "OK. Ivāga BP check māḍōṇa. ... BP 140 by 90 ide. Swalpa high ide.",
        "translated_text": "OK. Let's check BP now. ... BP is 140/90. It's slightly high.",
        "original_language": "kn-en",
        "start_time": 80.0,
        "end_time": 88.0,
        "confidence": 0.92,
    },
    {
        "id": "seg-022",
        "segment_index": 21,
        "speaker": "doctor",
        "text": "Nānu CBC and chest X-ray māḍisi anta hēḷtēne. Paracetamol 500 mg tablet koDtēne, ārū hours ge ondu tablet tagondi.",
        "translated_text": "I'll advise CBC and chest X-ray. I'll give you Paracetamol 500 mg tablet, take one tablet every six hours.",
        "original_language": "kn-en",
        "start_time": 89.0,
        "end_time": 98.0,
        "confidence": 0.90,
    },
    {
        "id": "seg-023",
        "segment_index": 22,
        "speaker": "doctor",
        "text": "Cough syrup ū koDtēne. Lots of fluids tagobēku. Rest māḍi. Two days nantara banni review ge.",
        "translated_text": "I'll also give cough syrup. You need to take lots of fluids. Take rest. Come back after two days for review.",
        "original_language": "kn-en",
        "start_time": 98.5,
        "end_time": 106.0,
        "confidence": 0.91,
    },
    {
        "id": "seg-024",
        "segment_index": 23,
        "speaker": "patient",
        "text": "Thank you doctor.",
        "translated_text": "Thank you doctor.",
        "original_language": "en",
        "start_time": 106.5,
        "end_time": 108.0,
        "confidence": 0.99,
    },
]

# ─── Primary Demo Clinical Extraction ─────────────────────

DEMO_CLINICAL_EXTRACTION = {
    "chief_complaints": [
        {
            "value": "Fever",
            "presence": "present",
            "confidence": 0.96,
            "source_segment_ids": ["seg-002"],
            "status": "ai_generated",
            "attributes": {"duration": "3 days", "onset": "Monday night", "max_temperature": "101.5°F"},
        }
    ],
    "symptoms": [
        {
            "value": "Cough",
            "presence": "present",
            "confidence": 0.94,
            "source_segment_ids": ["seg-008"],
            "status": "ai_generated",
            "attributes": {"type": "dry cough", "pattern": "worse at night", "severity": "moderate"},
        },
        {
            "value": "Running nose",
            "presence": "present",
            "confidence": 0.88,
            "source_segment_ids": ["seg-010"],
            "status": "ai_generated",
            "attributes": {"severity": "mild"},
        },
        {
            "value": "Body pain",
            "presence": "present",
            "confidence": 0.93,
            "source_segment_ids": ["seg-016"],
            "status": "ai_generated",
            "attributes": {},
        },
        {
            "value": "Headache",
            "presence": "present",
            "confidence": 0.90,
            "source_segment_ids": ["seg-016"],
            "status": "ai_generated",
            "attributes": {"severity": "mild"},
        },
    ],
    "negative_findings": [
        {
            "value": "Chest pain",
            "presence": "absent",
            "confidence": 0.96,
            "source_segment_ids": ["seg-012"],
            "status": "ai_generated",
            "attributes": {},
        },
        {
            "value": "Breathlessness",
            "presence": "absent",
            "confidence": 0.96,
            "source_segment_ids": ["seg-012"],
            "status": "ai_generated",
            "attributes": {},
        },
        {
            "value": "Vomiting",
            "presence": "absent",
            "confidence": 0.95,
            "source_segment_ids": ["seg-014"],
            "status": "ai_generated",
            "attributes": {},
        },
        {
            "value": "Loose stools",
            "presence": "absent",
            "confidence": 0.95,
            "source_segment_ids": ["seg-014"],
            "status": "ai_generated",
            "attributes": {},
        },
    ],
    "duration": [
        {
            "value": "3 days",
            "confidence": 0.96,
            "source_segment_ids": ["seg-002", "seg-004"],
            "status": "ai_generated",
            "attributes": {"onset": "Monday night"},
        }
    ],
    "medications": [
        {
            "value": "Amlodipine",
            "confidence": 0.91,
            "source_segment_ids": ["seg-020"],
            "status": "ai_generated",
            "attributes": {"dosage": "5 mg", "context": "current medication for hypertension"},
        },
        {
            "value": "Paracetamol",
            "confidence": 0.90,
            "source_segment_ids": ["seg-022"],
            "status": "ai_generated",
            "attributes": {"dosage": "500 mg", "frequency": "every 6 hours", "context": "prescribed"},
        },
        {
            "value": "Cough syrup",
            "confidence": 0.88,
            "source_segment_ids": ["seg-023"],
            "status": "ai_generated",
            "attributes": {"dosage": "Not specified", "context": "prescribed"},
        },
    ],
    "allergies": [
        {
            "value": "No known allergies",
            "presence": "absent",
            "confidence": 0.95,
            "source_segment_ids": ["seg-018"],
            "status": "ai_generated",
            "attributes": {"explicitly_stated": True},
        }
    ],
    "vitals": [
        {
            "value": "Blood pressure — 140/90 mmHg",
            "confidence": 0.92,
            "source_segment_ids": ["seg-021"],
            "status": "ai_generated",
            "attributes": {"systolic": 140, "diastolic": 90, "interpretation": "elevated"},
        },
        {
            "value": "Temperature — 101.5°F",
            "confidence": 0.95,
            "source_segment_ids": ["seg-006"],
            "status": "ai_generated",
            "attributes": {"reading": "101.5", "unit": "F", "timing": "yesterday"},
        },
    ],
    "examination_findings": [],
    "investigations": [
        {
            "value": "CBC",
            "confidence": 0.90,
            "source_segment_ids": ["seg-022"],
            "status": "ai_generated",
            "attributes": {"ordered_by": "doctor"},
        },
        {
            "value": "Chest X-ray",
            "confidence": 0.90,
            "source_segment_ids": ["seg-022"],
            "status": "ai_generated",
            "attributes": {"ordered_by": "doctor"},
        },
    ],
    "past_medical_history": [
        {
            "value": "Hypertension",
            "confidence": 0.91,
            "source_segment_ids": ["seg-020"],
            "status": "ai_generated",
            "attributes": {"duration": "diagnosed last year", "on_treatment": True},
        }
    ],
    "family_history": [
        {
            "value": "Not mentioned",
            "confidence": 0.0,
            "source_segment_ids": [],
            "status": "ai_generated",
            "attributes": {},
        }
    ],
    "social_history": [
        {
            "value": "Not mentioned",
            "confidence": 0.0,
            "source_segment_ids": [],
            "status": "ai_generated",
            "attributes": {},
        }
    ],
    "assessment": [
        {
            "value": "Acute febrile illness with upper respiratory symptoms — AI-generated suggestion, physician review required",
            "confidence": 0.78,
            "source_segment_ids": ["seg-002", "seg-008"],
            "status": "ai_generated",
            "attributes": {"is_suggestion": True},
        }
    ],
    "plan": [
        {
            "value": "Paracetamol 500 mg every 6 hours",
            "confidence": 0.90,
            "source_segment_ids": ["seg-022"],
            "status": "ai_generated",
            "attributes": {},
        },
        {
            "value": "Cough syrup (dosage not specified — doctor review required)",
            "confidence": 0.85,
            "source_segment_ids": ["seg-023"],
            "status": "ai_generated",
            "attributes": {},
        },
        {
            "value": "Adequate fluid intake",
            "confidence": 0.91,
            "source_segment_ids": ["seg-023"],
            "status": "ai_generated",
            "attributes": {},
        },
        {
            "value": "Rest",
            "confidence": 0.91,
            "source_segment_ids": ["seg-023"],
            "status": "ai_generated",
            "attributes": {},
        },
    ],
    "follow_up": [
        {
            "value": "Review after 2 days",
            "confidence": 0.91,
            "source_segment_ids": ["seg-023"],
            "status": "ai_generated",
            "attributes": {},
        }
    ],
    "uncertainties": [
        {
            "value": "Cough syrup dosage not explicitly mentioned",
            "confidence": 0.85,
            "source_segment_ids": ["seg-023"],
            "status": "ai_generated",
            "attributes": {"category": "missing_dosage"},
        }
    ],
}


# ─── Demo Clinical Note ──────────────────────────────────

DEMO_CLINICAL_NOTE = {
    "patient_info": {
        "name": "Rahul Kumar",
        "age": 42,
        "gender": "Male",
        "mrn": "MRN-2026-0001",
        "blood_group": "B+",
    },
    "chief_complaint": {
        "title": "Chief Complaint",
        "content": "Fever — 3 days",
        "entities": DEMO_CLINICAL_EXTRACTION["chief_complaints"],
        "status": "ai_generated",
    },
    "history_of_present_illness": {
        "title": "History of Present Illness",
        "content": "42-year-old male presents with fever of 3 days duration. Fever started on Monday night, initially mild, worsened from Tuesday. Highest recorded temperature was 101.5°F (yesterday). Associated with dry cough, worse at night. Mild running nose present. Body pain and mild headache present. Denies chest pain, breathlessness, vomiting, and loose stools.",
        "entities": [],
        "status": "ai_generated",
    },
    "associated_symptoms": {
        "title": "Associated Symptoms",
        "content": "Cough — dry, worse at night\nRunning nose — mild\nBody pain\nHeadache — mild",
        "entities": DEMO_CLINICAL_EXTRACTION["symptoms"],
        "status": "ai_generated",
    },
    "negative_findings": {
        "title": "Negative Findings",
        "content": "Chest pain — Absent\nBreathlessness — Absent\nVomiting — Absent\nLoose stools — Absent",
        "entities": DEMO_CLINICAL_EXTRACTION["negative_findings"],
        "status": "ai_generated",
    },
    "past_medical_history": {
        "title": "Past Medical History",
        "content": "Hypertension — diagnosed last year, on treatment",
        "entities": DEMO_CLINICAL_EXTRACTION["past_medical_history"],
        "status": "ai_generated",
    },
    "medication_history": {
        "title": "Medication History",
        "content": "Amlodipine 5 mg — current medication for hypertension",
        "entities": [DEMO_CLINICAL_EXTRACTION["medications"][0]],
        "status": "ai_generated",
    },
    "allergies": {
        "title": "Allergies",
        "content": "No known allergies (patient explicitly stated)",
        "entities": DEMO_CLINICAL_EXTRACTION["allergies"],
        "status": "ai_generated",
    },
    "vitals": {
        "title": "Vitals",
        "content": "Blood Pressure: 140/90 mmHg (elevated)\nTemperature: 101.5°F (recorded yesterday)",
        "entities": DEMO_CLINICAL_EXTRACTION["vitals"],
        "status": "ai_generated",
    },
    "examination": {
        "title": "Examination",
        "content": "Not documented in this encounter",
        "entities": [],
        "status": "ai_generated",
    },
    "investigations": {
        "title": "Investigations",
        "content": "CBC — ordered\nChest X-ray — ordered",
        "entities": DEMO_CLINICAL_EXTRACTION["investigations"],
        "status": "ai_generated",
    },
    "assessment": {
        "title": "Assessment",
        "content": "Acute febrile illness with upper respiratory symptoms — AI-generated suggestion, physician review required",
        "entities": DEMO_CLINICAL_EXTRACTION["assessment"],
        "status": "ai_generated",
    },
    "plan": {
        "title": "Plan",
        "content": "1. Paracetamol 500 mg every 6 hours\n2. Cough syrup (dosage not specified — doctor review required)\n3. Adequate fluid intake\n4. Rest\n5. Review after 2 days",
        "entities": DEMO_CLINICAL_EXTRACTION["plan"],
        "status": "ai_generated",
    },
    "follow_up": {
        "title": "Follow-up",
        "content": "Review after 2 days",
        "entities": DEMO_CLINICAL_EXTRACTION["follow_up"],
        "status": "ai_generated",
    },
}


# ─── Demo Evidence Links ─────────────────────────────────

DEMO_EVIDENCE_LINKS = [
    {
        "id": "evd-001",
        "field_path": "chief_complaint",
        "entity_value": "Fever — 3 days",
        "source_speaker": "patient",
        "source_text": "Doctor, nange three days inda fever ide.",
        "extraction_explanation": "Patient explicitly stated duration of fever as three days.",
        "confidence": 0.96,
        "transcript_segment_id": "seg-002",
    },
    {
        "id": "evd-002",
        "field_path": "associated_symptoms.cough",
        "entity_value": "Cough — dry, worse at night",
        "source_speaker": "patient",
        "source_text": "Yes doctor, cough ide. Night time alli jaasti agutte. Dry cough tarah ide.",
        "extraction_explanation": "Patient confirmed cough, described as dry type, with nocturnal worsening pattern.",
        "confidence": 0.94,
        "transcript_segment_id": "seg-008",
    },
    {
        "id": "evd-003",
        "field_path": "negative_findings.chest_pain",
        "entity_value": "Chest pain — Absent",
        "source_speaker": "patient",
        "source_text": "Illa doctor, chest pain illa. Breathlessness ū illa.",
        "extraction_explanation": "Patient explicitly denied chest pain and breathlessness. Negation detected.",
        "confidence": 0.96,
        "transcript_segment_id": "seg-012",
    },
    {
        "id": "evd-004",
        "field_path": "allergies",
        "entity_value": "No known allergies",
        "source_speaker": "patient",
        "source_text": "Illa doctor, yāvudē allergy illa nange.",
        "extraction_explanation": "Patient explicitly stated no allergies. This is not an AI inference — patient directly denied any allergies.",
        "confidence": 0.95,
        "transcript_segment_id": "seg-018",
    },
    {
        "id": "evd-005",
        "field_path": "vitals.blood_pressure",
        "entity_value": "BP: 140/90 mmHg",
        "source_speaker": "doctor",
        "source_text": "BP 140 by 90 ide. Swalpa high ide.",
        "extraction_explanation": "Doctor measured and stated BP reading during consultation.",
        "confidence": 0.92,
        "transcript_segment_id": "seg-021",
    },
    {
        "id": "evd-006",
        "field_path": "vitals.temperature",
        "entity_value": "Temperature: 101.5°F",
        "source_speaker": "patient",
        "source_text": "Hūdu doctor, 101 point 5 itta yesterday.",
        "extraction_explanation": "Patient reported highest temperature reading from previous day.",
        "confidence": 0.95,
        "transcript_segment_id": "seg-006",
    },
    {
        "id": "evd-007",
        "field_path": "past_medical_history.hypertension",
        "entity_value": "Hypertension — on Amlodipine 5 mg",
        "source_speaker": "patient",
        "source_text": "BP swalpa high ide anta last year hēḷidru. Tablet tagonttiddēne. Amlodipine 5 mg.",
        "extraction_explanation": "Patient reported existing hypertension diagnosis and current medication with explicit dosage.",
        "confidence": 0.91,
        "transcript_segment_id": "seg-020",
    },
    {
        "id": "evd-008",
        "field_path": "investigations",
        "entity_value": "CBC, Chest X-ray ordered",
        "source_speaker": "doctor",
        "source_text": "Nānu CBC and chest X-ray māḍisi anta hēḷtēne.",
        "extraction_explanation": "Doctor ordered investigations during consultation.",
        "confidence": 0.90,
        "transcript_segment_id": "seg-022",
    },
]


# ─── Demo Safety Flags ───────────────────────────────────

DEMO_SAFETY_FLAGS = [
    {
        "id": "sf-001",
        "severity": "warning",
        "category": "missing_dosage",
        "message": "⚠️ Cough syrup dosage not explicitly mentioned. AI will not infer dosage. Doctor review required.",
        "field_path": "plan.cough_syrup",
        "resolved": False,
    },
    {
        "id": "sf-002",
        "severity": "info",
        "category": "elevated_vital",
        "message": "Blood pressure reading 140/90 mmHg is elevated. Patient has known hypertension on Amlodipine 5 mg.",
        "field_path": "vitals.blood_pressure",
        "resolved": False,
    },
    {
        "id": "sf-003",
        "severity": "info",
        "category": "ai_suggestion",
        "message": "Assessment is an AI-generated suggestion. Physician review and confirmation required before finalization.",
        "field_path": "assessment",
        "resolved": False,
    },
    {
        "id": "sf-004",
        "severity": "info",
        "category": "incomplete_examination",
        "message": "Physical examination findings not documented in this encounter transcript.",
        "field_path": "examination",
        "resolved": False,
    },
    {
        "id": "sf-005",
        "severity": "info",
        "category": "family_history_missing",
        "message": "Family history not mentioned during consultation. AI did not infer family history.",
        "field_path": "family_history",
        "resolved": False,
    },
]


# ─── Demo Patient Summary ────────────────────────────────

DEMO_PATIENT_SUMMARY = {
    "consultation_id": "consult-demo-001",
    "patient_name": "Rahul Kumar",
    "visit_date": "08 October 2026",
    "what_you_told_the_doctor": [
        "Fever for 3 days (started Monday night)",
        "Cough — dry, worse at night",
        "Mild running nose",
        "Body pain and mild headache",
        "No chest pain",
        "No breathlessness",
        "No vomiting",
        "No known allergies",
        "Taking Amlodipine 5 mg for blood pressure",
    ],
    "doctors_instructions": [
        "Take Paracetamol 500 mg every 6 hours for fever",
        "Take cough syrup as prescribed",
        "Drink lots of fluids",
        "Take adequate rest",
    ],
    "medicines": [
        "Paracetamol 500 mg — every 6 hours",
        "Cough syrup — as prescribed by doctor",
    ],
    "tests": [
        "CBC (Complete Blood Count)",
        "Chest X-ray",
    ],
    "follow_up": "Come back after 2 days for review",
    "language": "Kannada + English",
    "disclaimer": "This summary is for your reference. Always follow your doctor's verbal instructions. This is not medical advice.",
}


# ─── Demo Timeline ────────────────────────────────────────

DEMO_TIMELINE = [
    {
        "id": "tl-001",
        "encounter_date": "2026-10-08",
        "chief_complaints": ["Fever — 3 days", "Cough — dry, nocturnal"],
        "vitals_snapshot": {"bp": "140/90 mmHg", "temperature": "101.5°F"},
        "summary": {
            "assessment": "Acute febrile illness with upper respiratory symptoms",
            "plan": "Paracetamol, cough syrup, fluids, rest",
            "investigations": "CBC, Chest X-ray ordered",
            "follow_up": "Review after 2 days",
        },
        "status": "final",
    },
]


# ─── Demo FHIR Resources ─────────────────────────────────

DEMO_FHIR_PATIENT = {
    "resourceType": "Patient",
    "id": "pat-demo-001",
    "identifier": [
        {
            "system": "https://clinscribe.ai/mrn",
            "value": "MRN-2026-0001",
        }
    ],
    "name": [
        {
            "use": "official",
            "family": "Kumar",
            "given": ["Rahul"],
        }
    ],
    "gender": "male",
    "birthDate": "1984-05-15",
}

DEMO_FHIR_ENCOUNTER = {
    "resourceType": "Encounter",
    "id": "consult-demo-001",
    "status": "finished",
    "class": {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
        "code": "AMB",
        "display": "ambulatory",
    },
    "subject": {"reference": "Patient/pat-demo-001"},
    "period": {
        "start": "2026-10-08T10:00:00+05:30",
        "end": "2026-10-08T10:15:00+05:30",
    },
}

DEMO_FHIR_CONDITIONS = [
    {
        "resourceType": "Condition",
        "id": "cond-001",
        "clinicalStatus": {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]
        },
        "code": {"text": "Fever"},
        "subject": {"reference": "Patient/pat-demo-001"},
        "encounter": {"reference": "Encounter/consult-demo-001"},
        "onsetString": "3 days ago",
    },
    {
        "resourceType": "Condition",
        "id": "cond-002",
        "clinicalStatus": {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]
        },
        "code": {"text": "Dry cough"},
        "subject": {"reference": "Patient/pat-demo-001"},
        "encounter": {"reference": "Encounter/consult-demo-001"},
        "note": [{"text": "Worse at night"}],
    },
]

DEMO_FHIR_OBSERVATIONS = [
    {
        "resourceType": "Observation",
        "id": "obs-001",
        "status": "final",
        "code": {"text": "Blood Pressure"},
        "subject": {"reference": "Patient/pat-demo-001"},
        "encounter": {"reference": "Encounter/consult-demo-001"},
        "component": [
            {
                "code": {"text": "Systolic Blood Pressure"},
                "valueQuantity": {"value": 140, "unit": "mmHg"},
            },
            {
                "code": {"text": "Diastolic Blood Pressure"},
                "valueQuantity": {"value": 90, "unit": "mmHg"},
            },
        ],
    },
    {
        "resourceType": "Observation",
        "id": "obs-002",
        "status": "final",
        "code": {"text": "Body Temperature"},
        "subject": {"reference": "Patient/pat-demo-001"},
        "encounter": {"reference": "Encounter/consult-demo-001"},
        "valueQuantity": {"value": 101.5, "unit": "°F"},
    },
]

DEMO_FHIR_MEDICATION_REQUESTS = [
    {
        "resourceType": "MedicationRequest",
        "id": "medrq-001",
        "status": "active",
        "intent": "order",
        "medicationCodeableConcept": {"text": "Paracetamol 500 mg"},
        "subject": {"reference": "Patient/pat-demo-001"},
        "encounter": {"reference": "Encounter/consult-demo-001"},
        "dosageInstruction": [
            {
                "text": "500 mg every 6 hours",
                "timing": {"repeat": {"frequency": 4, "period": 1, "periodUnit": "d"}},
            }
        ],
    },
]

DEMO_FHIR_BUNDLE = {
    "resourceType": "Bundle",
    "type": "collection",
    "entry": [
        {"resource": DEMO_FHIR_PATIENT},
        {"resource": DEMO_FHIR_ENCOUNTER},
        *[{"resource": c} for c in DEMO_FHIR_CONDITIONS],
        *[{"resource": o} for o in DEMO_FHIR_OBSERVATIONS],
        *[{"resource": m} for m in DEMO_FHIR_MEDICATION_REQUESTS],
    ],
}


# ─── Demo Evaluation Metrics ─────────────────────────────

DEMO_EVALUATION_METRICS = {
    "asr_metrics": {
        "word_error_rate": None,
        "character_error_rate": None,
        "samples_evaluated": 0,
        "status": "Evaluation in progress — synthetic demo data",
    },
    "extraction_metrics": {
        "precision": None,
        "recall": None,
        "f1_score": None,
        "samples_evaluated": 0,
        "status": "Evaluation in progress — synthetic demo data",
    },
    "workflow_metrics": {
        "avg_documentation_time_seconds": None,
        "avg_doctor_correction_time_seconds": None,
        "correction_rate": None,
        "documentation_time_saved_pct": None,
        "status": "Not yet measured",
    },
    "unsupported_information_rate": None,
    "total_consultations_evaluated": 0,
    "last_evaluation": None,
}


# ─── Specialty Templates ─────────────────────────────────

SPECIALTY_TEMPLATES = {
    "general_medicine": {
        "name": "General Medicine",
        "sections": [
            "chief_complaint", "history_of_present_illness", "associated_symptoms",
            "negative_findings", "past_medical_history", "medication_history",
            "allergies", "vitals", "examination", "investigations",
            "assessment", "plan", "follow_up",
        ],
        "focus_entities": [
            "fever", "cough", "cold", "body_pain", "headache", "weakness",
            "appetite", "sleep", "bowel_habits", "urinary_complaints",
        ],
    },
    "pediatrics": {
        "name": "Pediatrics",
        "sections": [
            "chief_complaint", "history_of_present_illness", "associated_symptoms",
            "negative_findings", "birth_history", "feeding_history",
            "vaccination_status", "developmental_milestones", "growth_parameters",
            "past_medical_history", "medication_history", "allergies",
            "vitals", "examination", "investigations", "assessment", "plan", "follow_up",
        ],
        "focus_entities": [
            "age", "weight", "height", "fever", "feeding", "vaccination",
            "growth", "development", "birth_weight",
        ],
    },
    "orthopedics": {
        "name": "Orthopedics",
        "sections": [
            "chief_complaint", "history_of_present_illness", "pain_assessment",
            "injury_details", "associated_symptoms", "negative_findings",
            "past_medical_history", "medication_history", "allergies",
            "vitals", "musculoskeletal_examination", "range_of_motion",
            "investigations", "assessment", "plan", "follow_up",
        ],
        "focus_entities": [
            "pain_location", "pain_severity", "injury", "trauma", "swelling",
            "range_of_motion", "duration", "onset", "aggravating_factors",
        ],
    },
    "ent": {
        "name": "ENT",
        "sections": [
            "chief_complaint", "history_of_present_illness", "associated_symptoms",
            "negative_findings", "past_medical_history", "medication_history",
            "allergies", "vitals", "ent_examination", "investigations",
            "assessment", "plan", "follow_up",
        ],
        "focus_entities": [
            "ear_pain", "hearing_loss", "tinnitus", "vertigo",
            "nasal_obstruction", "rhinorrhea", "sore_throat",
            "hoarseness", "dysphagia",
        ],
    },
    "dermatology": {
        "name": "Dermatology",
        "sections": [
            "chief_complaint", "history_of_present_illness", "lesion_description",
            "associated_symptoms", "negative_findings", "past_medical_history",
            "medication_history", "allergies", "vitals", "dermatological_examination",
            "investigations", "assessment", "plan", "follow_up",
        ],
        "focus_entities": [
            "rash", "itching", "lesion_type", "location", "distribution",
            "duration", "progression", "previous_treatment",
        ],
    },
    "gynecology": {
        "name": "Gynecology",
        "sections": [
            "chief_complaint", "history_of_present_illness", "menstrual_history",
            "obstetric_history", "associated_symptoms", "negative_findings",
            "past_medical_history", "medication_history", "allergies",
            "vitals", "examination", "investigations", "assessment", "plan", "follow_up",
        ],
        "focus_entities": [
            "menstrual_cycle", "last_menstrual_period", "parity",
            "vaginal_discharge", "pelvic_pain", "contraception",
        ],
    },
    "cardiology": {
        "name": "Cardiology",
        "sections": [
            "chief_complaint", "history_of_present_illness", "cardiac_symptoms",
            "associated_symptoms", "negative_findings", "cardiac_risk_factors",
            "past_medical_history", "medication_history", "allergies",
            "vitals", "cardiovascular_examination", "investigations",
            "assessment", "plan", "follow_up",
        ],
        "focus_entities": [
            "chest_pain", "palpitations", "dyspnea", "syncope",
            "edema", "claudication", "hypertension", "diabetes",
        ],
    },
}
