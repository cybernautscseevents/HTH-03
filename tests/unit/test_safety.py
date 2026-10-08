"""
ClinScribe AI — Unit Tests for Safety Engine
Tests drug allergy detection, red flags, and contraindications.
"""

import sys
import os
import unittest

# Ensure service paths are included
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'services', 'safety')))
from safety_service import SafetyEngine


class TestSafetyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SafetyEngine()

    def test_allergy_detection(self):
        prescribed = ["Amoxicillin 500mg TDS", "Paracetamol 650mg"]
        allergies = ["Penicillin"]
        issues = self.engine.check_drug_allergies(prescribed, allergies)
        self.assertTrue(len(issues) > 0)
        self.assertEqual(issues[0].severity, "critical")
        self.assertIn("Amoxicillin", issues[0].description)

    def test_red_flag_detection(self):
        transcript = "Doctor sir, I have severe chest pain and left arm pain with sweating."
        issues = self.engine.check_red_flags(transcript)
        self.assertTrue(len(issues) > 0)
        self.assertEqual(issues[0].severity, "critical")
        self.assertIn("Acute Coronary Syndrome", issues[0].description)

    def test_kannada_indic_red_flag(self):
        transcript = "Edeya novu tumba aagide mathu chakkar barthide doctor."
        issues = self.engine.check_red_flags(transcript)
        self.assertTrue(len(issues) > 0)

    def test_contraindication(self):
        diagnoses = ["Type 2 Diabetes", "Chronic Kidney Disease Stage 4"]
        meds = ["Metformin 500mg BD", "Amlodipine 5mg"]
        issues = self.engine.check_contraindications(diagnoses, meds)
        self.assertTrue(len(issues) > 0)
        self.assertEqual(issues[0].severity, "high")


if __name__ == "__main__":
    unittest.main()
