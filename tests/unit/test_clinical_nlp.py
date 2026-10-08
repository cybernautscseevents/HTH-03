"""
ClinScribe AI — Unit Tests for Clinical NLP Pipeline & FHIR Converter
"""

import sys
import os
import unittest
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'services', 'clinical-nlp')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'services', 'fhir')))

from clinical_nlp_service import ClinicalNLPPipeline, extract_symptoms_from_text, extract_vitals_from_text
from fhir_service import FHIRConverter


class TestClinicalNLPAndFHIR(unittest.TestCase):
    def setUp(self):
        self.pipeline = ClinicalNLPPipeline(use_llm=False)
        self.fhir = FHIRConverter()

    def test_symptom_extraction(self):
        text = "Patient complains of chest pain since 2 weeks and fever."
        symptoms = extract_symptoms_from_text(text, "seg-1", "patient")
        self.assertTrue(len(symptoms) >= 1)
        names = [s.value.lower() for s in symptoms]
        self.assertTrue(any("chest pain" in n or "fever" in n for n in names))

    def test_vital_extraction(self):
        text = "BP measured today is 150/95 mmHg, pulse rate 88."
        vitals = extract_vitals_from_text(text, "seg-2", "doctor")
        self.assertTrue(len(vitals) >= 1)
        bp_found = any(v.entity_type == "vital" and "150/95" in v.value for v in vitals)
        self.assertTrue(bp_found)

    def test_pipeline_async_extract(self):
        segments = [
            {"id": "seg-1", "speaker": "patient", "text": "I have severe fever and cough."},
            {"id": "seg-2", "speaker": "doctor", "text": "BP is 130/80 mmHg."}
        ]
        result = asyncio.run(self.pipeline.extract_entities(segments))
        self.assertIn("symptoms", result)
        self.assertIn("vitals", result)
        self.assertTrue(len(result["symptoms"]) > 0)
        self.assertTrue(len(result["vitals"]) > 0)

    def test_fhir_bundle_generation(self):
        patient = {"id": "pat-123", "full_name": "Ramesh Kumar", "gender": "male", "abha_id": "91-1234-5678-9012"}
        doctor = {"id": "doc-456", "full_name": "Dr. Sneha Rao", "specialty": "Cardiology"}
        consultation = {"id": "enc-789", "created_at": "2026-10-08T10:00:00Z"}
        clinical_note = {
            "soap_sections": {
                "assessment": {"diagnoses": ["Essential Hypertension"]},
                "plan": {"medications": [{"name": "Amlodipine 5mg", "dosage": "1 OD"}]}
            }
        }
        bundle = self.fhir.build_bundle(patient, doctor, consultation, clinical_note)
        self.assertEqual(bundle["resourceType"], "Bundle")
        self.assertEqual(bundle["type"], "document")
        self.assertTrue(len(bundle["entry"]) >= 4)


if __name__ == "__main__":
    unittest.main()
