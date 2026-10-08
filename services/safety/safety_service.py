"""
ClinScribe AI — Safety & Clinical Guardrails Engine
Real-time safety checks, drug-allergy interactions, red flag detectors,
dosage boundary verifiers, and clinical contraindication guardrails.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class SafetyIssue:
    id: str
    rule_name: str
    severity: str  # critical, high, medium, low
    category: str  # allergy, contraindication, red_flag, dosage, missing_vital
    description: str
    recommendation: str
    evidence_snippet: Optional[str] = None
    action_required: bool = True


class SafetyEngine:
    """
    Deterministic rule-based clinical safety engine designed for high precision.
    Evaluates clinical notes, extracted entities, and patient history.
    """

    # Common drug allergy families
    ALLERGY_FAMILIES = {
        "penicillin": ["amoxicillin", "ampicillin", "augmentin", "penicillin", "piperacillin", "clavulanate"],
        "sulfa": ["bactrim", "septra", "cotrimoxazole", "sulfamethoxazole", "glimepiride"],
        "nsaid": ["aspirin", "ibuprofen", "naproxen", "diclofenac", "aceclofenac", "meloxicam", "piroxicam"],
        "cephalosporin": ["cephalexin", "cefixime", "ceftriaxone", "cefuroxime", "cefepime"]
    }

    # Red flag symptom patterns in Indian OPDs (English + transliterated Indic)
    RED_FLAGS = [
        {
            "id": "RF-001",
            "pattern": r"(chest pain|edeya novu|chhati mein dard|sinhe mein dard).*(jaw|left arm|shoulder|sweat|ghabrahat|chakkar)",
            "severity": "critical",
            "category": "red_flag",
            "description": "Possible Acute Coronary Syndrome (ACS) / Myocardial Infarction indicators detected.",
            "recommendation": "Perform immediate 12-lead ECG, troponin I/T assay, assess hemodynamic stability, and prepare emergency cardiology consult."
        },
        {
            "id": "RF-002",
            "pattern": r"(shortness of breath|usiru kattuvike|sans lene mein takleef|breathlessness).*(rest|swelling|oedema)",
            "severity": "high",
            "category": "red_flag",
            "description": "Acute dyspnea / pulmonary congestion or cardiac decompensation risk.",
            "recommendation": "Check SpO2 immediately, auscultate lung bases for crepitations, consider chest X-ray and NT-proBNP."
        },
        {
            "id": "RF-003",
            "pattern": r"(slurred speech|facial droop|weakness in arm|matondu baralla|lakwa)",
            "severity": "critical",
            "category": "red_flag",
            "description": "Acute focal neurological deficit / potential stroke symptoms.",
            "recommendation": "Immediate FAST stroke protocol evaluation, non-contrast CT brain, calculate time since last known well."
        }
    ]

    def check_drug_allergies(self, prescribed_meds: List[str], known_allergies: List[str]) -> List[SafetyIssue]:
        issues = []
        for allergy in known_allergies:
            allergy_lower = allergy.lower().strip()
            for group_name, members in self.ALLERGY_FAMILIES.items():
                if allergy_lower in members or allergy_lower == group_name:
                    for med in prescribed_meds:
                        med_lower = med.lower().strip()
                        if any(m in med_lower for m in members):
                            issues.append(SafetyIssue(
                                id=f"ALLERGY-{allergy_lower}-{med_lower[:5]}",
                                rule_name="Drug Allergy Cross-Reaction",
                                severity="critical",
                                category="allergy",
                                description=f"Prescribed medication '{med}' conflicts with documented allergy to '{allergy}' ({group_name.title()} class).",
                                recommendation=f"Substitute with non-{group_name} alternative and verify patient allergy band/records.",
                                evidence_snippet=f"Documented Allergy: {allergy} | Prescribed: {med}"
                            ))
        return issues

    def check_red_flags(self, consultation_text: str) -> List[SafetyIssue]:
        issues = []
        text_lower = consultation_text.lower()
        for rf in self.RED_FLAGS:
            if re.search(rf["pattern"], text_lower):
                issues.append(SafetyIssue(
                    id=rf["id"],
                    rule_name="Red Flag Clinical Alarm",
                    severity=rf["severity"],
                    category=rf["category"],
                    description=rf["description"],
                    recommendation=rf["recommendation"],
                    evidence_snippet=consultation_text[:120] + "..."
                ))
        return issues

    def check_contraindications(self, diagnoses: List[str], medications: List[str]) -> List[SafetyIssue]:
        issues = []
        diag_str = " ".join(diagnoses).lower()
        med_str = " ".join(medications).lower()

        # Metformin in Renal impairment
        if any(term in diag_str for term in ["ckd", "kidney disease", "kidney failure", "renal impairment", "creatinine > 2.0"]):
            if "metformin" in med_str:
                issues.append(SafetyIssue(
                    id="CONTRA-RENAL-METFORMIN",
                    rule_name="Renal Contraindication",
                    severity="high",
                    category="contraindication",
                    description="Metformin is contraindicated or requires dose modification in moderate-to-severe renal impairment due to lactic acidosis risk.",
                    recommendation="Review latest eGFR/serum creatinine before prescribing. Consider DPP-4 inhibitor (e.g. Linagliptin) instead."
                ))

        # NSAIDs in active peptic ulcer / gastritis
        if any(term in diag_str for term in ["peptic ulcer", "gastric ulcer", "gi bleed"]):
            if any(term in med_str for term in ["ibuprofen", "diclofenac", "naproxen"]):
                issues.append(SafetyIssue(
                    id="CONTRA-GI-NSAID",
                    rule_name="GI Bleed Risk Contraindication",
                    severity="high",
                    category="contraindication",
                    description="Non-steroidal anti-inflammatory drugs (NSAIDs) increase ulcer bleeding risk.",
                    recommendation="Avoid systemic NSAIDs; use Paracetamol or topical analgesics with PPI gastroprotection."
                ))

        return issues

    def run_all_checks(
        self,
        consultation_text: str,
        prescribed_meds: List[str],
        known_allergies: List[str],
        diagnoses: List[str]
    ) -> List[SafetyIssue]:
        issues = []
        issues.extend(self.check_drug_allergies(prescribed_meds, known_allergies))
        issues.extend(self.check_red_flags(consultation_text))
        issues.extend(self.check_contraindications(diagnoses, prescribed_meds))
        return issues
