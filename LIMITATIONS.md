# ClinScribe AI — Limitations

## Transparency Statement

ClinScribe AI is a hackathon prototype. This document transparently states known limitations.

## Speech Recognition

- ASR performance varies significantly by accent, dialect, and background noise
- Medical terminology can be misrecognized, especially when mixed with colloquial speech
- Code-mixed language (e.g., Kannada + English) is inherently challenging for ASR systems
- Performance in noisy OPD environments has not been validated
- Not all Indian languages are currently supported
- Whispered or very soft speech may not be captured accurately

## Clinical Entity Extraction

- Rule-based extraction may miss complex or unusual symptom descriptions
- Context-dependent clinical meaning may be lost
- Temporal relationships between symptoms may not be accurately captured
- Medical abbreviations coverage is not exhaustive
- Sarcasm, metaphors, and indirect expressions are not handled

## Negation Detection

- Complex multi-clause negation may be missed
- Code-mixed negation patterns are limited to common expressions
- Double negation handling is not robust
- Implied negation (without explicit negation words) is not detected

## Clinical Note Generation

- AI-generated notes are drafts and require physician review
- Assessment suggestions are not clinical diagnoses
- Note formatting may not match specific institutional standards
- Specialty-specific templates are basic and need customization

## Code-Mixed Language

- Only common code-mixing patterns are currently handled
- Script mixing (e.g., Devanagari + Latin) is not supported
- Regional dialect variations may not be recognized
- Slang and colloquial medical terms may be missed

## Safety

- Safety guard is rule-based and cannot catch all possible errors
- Does not replace clinical judgment
- Cannot verify factual accuracy of patient statements
- May not detect all contradictions in complex conversations

## Data

- **Demo data is entirely synthetic** — no real patient data is used
- Evaluation metrics are based on synthetic test cases only
- Real-world performance has not been validated
- Statistical metrics may not reflect actual clinical performance

## Privacy & Compliance

- Prototype has not undergone formal security audit
- Not compliant with any regulatory framework (HIPAA, ABDM, etc.)
- Production deployment requires comprehensive privacy impact assessment
- Data encryption is configurable but not enforced in demo mode

## Deployment

- Real-world deployment requires:
  - Clinical validation studies
  - Regulatory compliance assessment
  - Security audit and penetration testing
  - Performance testing under real OPD conditions
  - Integration testing with hospital information systems
  - User training and change management

## Not Intended For

- **Autonomous medical diagnosis or treatment**
- **Replacing physician clinical judgment**
- **Use with real patient data without proper compliance**
- **Production healthcare environments without clinical validation**
- **Emergency or critical care situations**
- **Prescribing medication without physician oversight**
