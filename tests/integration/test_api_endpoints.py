"""
ClinScribe AI — Integration Tests for FastAPI Endpoints
Tests full API surface with FastAPI TestClient.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'apps', 'api')))

from fastapi.testclient import TestClient
from main import app


class TestApiEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("ClinScribe AI", data["service"])

    def test_auth_login(self):
        response = self.client.post("/api/auth/login", json={
            "email": "dr.priya@clinscribe.demo",
            "password": "demo123"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["token_type"], "bearer")

    def test_list_patients(self):
        response = self.client.get("/api/patients")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("patients", data)
        self.assertTrue(len(data["patients"]) > 0)
        self.assertIn("first_name", data["patients"][0])

    def test_get_patient_detail(self):
        response = self.client.get("/api/patients/pat-demo-001")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], "pat-demo-001")
        self.assertEqual(data["first_name"], "Rahul")

    def test_get_consultation_detail(self):
        response = self.client.get("/api/consultations/consult-demo-001")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], "consult-demo-001")
        self.assertIn("doctor_id", data)

    def test_get_transcript(self):
        response = self.client.get("/api/consultations/consult-demo-001/transcript")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("segments", data)
        self.assertTrue(len(data["segments"]) > 0)

    def test_get_clinical_note(self):
        response = self.client.get("/api/consultations/consult-demo-001/clinical-note")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("content", data)
        self.assertIn("chief_complaint", data["content"])

    def test_get_evidence_links(self):
        response = self.client.get("/api/consultations/consult-demo-001/evidence")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("evidence_links", data)

    def test_get_safety_flags(self):
        response = self.client.get("/api/consultations/consult-demo-001/safety-flags")
        self.assertIn(response.status_code, [200, 404])

    def test_get_fhir_export(self):
        response = self.client.get("/api/consultations/consult-demo-001/fhir")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["fhir_bundle"]["resourceType"], "Bundle")

    def test_evaluation_dashboard(self):
        response = self.client.get("/api/evaluation/dashboard")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("asr_metrics", data)
        self.assertIn("extraction_metrics", data)


if __name__ == "__main__":
    unittest.main()
