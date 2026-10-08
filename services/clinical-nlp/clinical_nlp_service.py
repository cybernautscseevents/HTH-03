"""
ClinScribe AI — Clinical NLP Pipeline
Extracts clinical entities from transcripts with:
- Code-mixed language understanding
- Negation detection
- Speaker attribution
- Evidence linking
- Confidence scoring
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# ─── Negation Detection ──────────────────────────────────

NEGATION_PATTERNS = [
    # English patterns
    r'\bno\b\s+(\w[\w\s]*)',
    r'\bnot\b\s+(\w[\w\s]*)',
    r'\bdon\'?t\s+have\b\s+(\w[\w\s]*)',
    r'\bdoesn\'?t\s+have\b\s+(\w[\w\s]*)',
    r'\bdenies?\b\s+(\w[\w\s]*)',
    r'\bwithout\b\s+(\w[\w\s]*)',
    r'\babsence\s+of\b\s+(\w[\w\s]*)',
    r'\bnever\b\s+(\w[\w\s]*)',
    r'\bnone\b',
    r'\bnegative\s+for\b\s+(\w[\w\s]*)',
    # Kannada patterns (transliterated)
    r'\billa\b',  # "no" / "not there"
    r'\billā\b',
    r'\billada\b',
    r'\bāgilla\b',
    r'\bāgillā\b',
    # Hindi patterns (transliterated)
    r'\bnahi\b',
    r'\bnahīṁ\b',
    r'\bnhin\b',
    r'\bmat\b',
]

NEGATION_REGEX = re.compile('|'.join(NEGATION_PATTERNS), re.IGNORECASE)

# Clinical entity patterns
SYMPTOM_KEYWORDS = [
    "fever", "cough", "cold", "headache", "head pain", "body pain",
    "chest pain", "breathlessness", "vomiting", "nausea", "loose stools",
    "diarrhea", "constipation", "abdominal pain", "stomach pain",
    "sore throat", "running nose", "rhinorrhea", "weakness", "fatigue",
    "dizziness", "vertigo", "palpitations", "swelling", "rash",
    "itching", "weight loss", "weight gain", "appetite loss",
    "difficulty swallowing", "bleeding", "pain", "burning sensation",
]

VITAL_PATTERNS = [
    r'(?:bp|blood\s*pressure)\b[^0-9\n]{0,25}?(\d{2,3})\s*(?:by|/|over)\s*(\d{2,3})',
    r'(?:temperature|temp)\b[^0-9\n]{0,20}?(\d{2,3}(?:\.\d)?)\s*(?:°?[fc])?',
    r'(?:pulse|hr|heart\s*rate)\b[^0-9\n]{0,20}?(\d{2,3})',
    r'(?:spo2|oxygen|sat)\b[^0-9\n]{0,20}?(\d{2,3})\s*%?',
    r'(?:rr|respiratory\s*rate)\b[^0-9\n]{0,20}?(\d{1,2})',
]

DURATION_PATTERNS = [
    r'(\d+)\s*(?:days?|din)',
    r'(\d+)\s*(?:weeks?|hafta)',
    r'(\d+)\s*(?:months?|mahina)',
    r'(\d+)\s*(?:years?|saal|varsha)',
    r'(\d+)\s*(?:hours?|ghanta)',
]

MEDICATION_PATTERNS = [
    r'(?:tab(?:let)?\.?\s+)(\w+(?:\s+\d+\s*(?:mg|g|ml|mcg))?\b)',
    r'(\w+(?:ol|in|ide|ine|ate|one|fen|min|cin|zol|pam|lam)\b)',
]


@dataclass
class ExtractedEntity:
    """A clinical entity extracted from transcript."""
    entity_type: str
    value: str
    presence: str = "present"  # present, absent, unknown
    confidence: float = 0.0
    source_segment_ids: List[str] = field(default_factory=list)
    source_speaker: str = "unknown"
    source_text: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)


def detect_negation(text: str) -> bool:
    """Detect if the text contains negation."""
    return bool(NEGATION_REGEX.search(text.lower()))


def extract_symptoms_from_text(text: str, segment_id: str, speaker: str) -> List[ExtractedEntity]:
    """Extract symptom entities from a text segment."""
    entities = []
    text_lower = text.lower()
    is_negated = detect_negation(text_lower)

    for symptom in SYMPTOM_KEYWORDS:
        if symptom.lower() in text_lower:
            entity = ExtractedEntity(
                entity_type="symptom",
                value=symptom.title(),
                presence="absent" if is_negated else "present",
                confidence=0.85 if not is_negated else 0.90,
                source_segment_ids=[segment_id],
                source_speaker=speaker,
                source_text=text,
            )
            entities.append(entity)

    return entities


def extract_vitals_from_text(text: str, segment_id: str, speaker: str) -> List[ExtractedEntity]:
    """Extract vital signs from text."""
    entities = []

    for pattern in VITAL_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            if "bp" in pattern.lower() or "blood" in pattern.lower():
                entity = ExtractedEntity(
                    entity_type="vital",
                    value=f"Blood Pressure: {match.group(1)}/{match.group(2)} mmHg",
                    confidence=0.92,
                    source_segment_ids=[segment_id],
                    source_speaker=speaker,
                    source_text=text,
                    attributes={
                        "systolic": int(match.group(1)),
                        "diastolic": int(match.group(2)),
                    },
                )
                entities.append(entity)
            elif "temp" in pattern.lower():
                entity = ExtractedEntity(
                    entity_type="vital",
                    value=f"Temperature: {match.group(1)}°F",
                    confidence=0.93,
                    source_segment_ids=[segment_id],
                    source_speaker=speaker,
                    source_text=text,
                )
                entities.append(entity)

    return entities


def extract_duration_from_text(text: str, segment_id: str, speaker: str) -> List[ExtractedEntity]:
    """Extract duration information."""
    entities = []
    for pattern in DURATION_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            entity = ExtractedEntity(
                entity_type="duration",
                value=match.group(0),
                confidence=0.88,
                source_segment_ids=[segment_id],
                source_speaker=speaker,
                source_text=text,
            )
            entities.append(entity)
    return entities


class ClinicalNLPPipeline:
    """
    Main clinical NLP pipeline.
    Processes transcript segments and extracts structured clinical information.
    """

    def __init__(self, use_llm: bool = False, llm_provider: str = "demo"):
        self.use_llm = use_llm
        self.llm_provider = llm_provider
        logger.info(f"Clinical NLP pipeline initialized (use_llm: {use_llm})")

    async def extract_entities(
        self,
        segments: List[Dict[str, Any]],
    ) -> Dict[str, List[ExtractedEntity]]:
        """
        Extract all clinical entities from transcript segments.
        
        Returns categorized entities with source references.
        """
        all_symptoms = []
        all_negatives = []
        all_vitals = []
        all_durations = []
        all_medications = []

        for seg in segments:
            text = seg.get("text", "")
            seg_id = seg.get("id", "")
            speaker = seg.get("speaker", "unknown")

            # Extract symptoms (with negation detection)
            symptoms = extract_symptoms_from_text(text, seg_id, speaker)
            for s in symptoms:
                if s.presence == "absent":
                    all_negatives.append(s)
                else:
                    all_symptoms.append(s)

            # Extract vitals
            vitals = extract_vitals_from_text(text, seg_id, speaker)
            all_vitals.extend(vitals)

            # Extract durations
            durations = extract_duration_from_text(text, seg_id, speaker)
            all_durations.extend(durations)

        return {
            "symptoms": all_symptoms,
            "negative_findings": all_negatives,
            "vitals": all_vitals,
            "durations": all_durations,
            "medications": all_medications,
        }

    async def generate_clinical_note(
        self,
        extraction: Dict[str, Any],
        patient_info: Dict[str, Any],
        template_type: str = "general_medicine",
    ) -> Dict[str, Any]:
        """
        Generate a structured clinical note from extracted entities.
        
        In production: uses LLM for natural language generation.
        In demo: uses pre-built demo data.
        """
        if self.llm_provider == "demo":
            from demo_data import DEMO_CLINICAL_NOTE
            return DEMO_CLINICAL_NOTE

        # Production LLM integration would go here
        raise NotImplementedError("LLM clinical note generation not yet implemented")


class DemoClinicalNLPPipeline(ClinicalNLPPipeline):
    """Demo pipeline that returns pre-built clinical extraction."""

    def __init__(self):
        super().__init__(use_llm=False, llm_provider="demo")

    async def extract_entities(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Return demo extraction data."""
        from demo_data import DEMO_CLINICAL_EXTRACTION
        return DEMO_CLINICAL_EXTRACTION

    async def generate_clinical_note(
        self,
        extraction: Dict[str, Any],
        patient_info: Dict[str, Any],
        template_type: str = "general_medicine",
    ) -> Dict[str, Any]:
        from demo_data import DEMO_CLINICAL_NOTE
        return DEMO_CLINICAL_NOTE
