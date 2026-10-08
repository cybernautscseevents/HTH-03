# ClinScribe AI — Model Card

## Model Overview

ClinScribe AI uses a pipeline of AI models for ambient clinical documentation.

## ASR Model — AI4Bharat IndicConformer

- **Architecture**: Conformer-based end-to-end ASR
- **Source**: https://github.com/AI4Bharat/IndicConformerASR
- **License**: MIT
- **Languages**: Kannada, Hindi, Tamil, Telugu, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Odia, Assamese, Urdu, Sanskrit, English
- **Training Data**: IndicSUPERB and other Indian language speech corpora
- **Intended Use**: Indian language speech recognition in clinical settings
- **Limitations**:
  - Performance varies by accent, dialect, and noise level
  - Medical terminology may be misrecognized
  - Code-mixed speech is challenging
  - Background noise in OPD environments affects accuracy

## Whisper (Fallback)

- **Architecture**: Transformer-based multi-task ASR
- **Source**: OpenAI
- **License**: MIT
- **Intended Use**: Fallback ASR when IndicConformer is unavailable
- **Limitations**:
  - Not specifically trained on Indian languages
  - Code-mixed speech support is limited
  - Higher latency than IndicConformer for Indian languages

## Clinical NLP Pipeline

- **Type**: Hybrid rule-based + pattern matching
- **Capabilities**:
  - Symptom extraction
  - Vital sign parsing
  - Medication detection
  - Negation detection
  - Duration extraction
  - Speaker attribution
- **Intended Use**: Extracting structured clinical entities from conversation transcripts
- **Limitations**:
  - Rule-based extraction may miss complex or unusual expressions
  - Medical abbreviations may not all be covered
  - Context-dependent interpretation is limited
  - Not trained on real clinical data (prototype uses synthetic data)

## Clinical Safety Guard

- **Type**: Rule-based validation engine
- **Checks**:
  - Missing information detection
  - Medication dosage validation
  - Speaker attribution verification
  - Assessment confidence scoring
  - Hallucination detection (unsupported claims)
- **Intended Use**: Pre-approval safety validation of AI-generated clinical notes
- **Limitations**:
  - Cannot catch all possible errors
  - Does not replace clinical judgment
  - Rule coverage is not exhaustive

## Evaluation

### Metrics Tracked
- ASR: Word Error Rate (WER), Character Error Rate (CER)
- Extraction: Precision, Recall, F1-Score
- Note Generation: Completeness, factual consistency
- Workflow: Documentation time, doctor correction rate

### Current Status
- Evaluation in progress with synthetic demo data
- No real clinical validation performed
- Production deployment requires clinical validation study

## Ethical Considerations

- **Not a medical device**: This is a documentation assistant, not a diagnostic tool
- **Doctor remains in control**: All AI output requires explicit doctor approval
- **Transparency**: Evidence linking shows source for every AI-generated field
- **No autonomous prescribing**: AI never independently prescribes medication
- **Bias considerations**: Model performance may vary across languages, accents, and demographics
- **Data privacy**: Designed for healthcare data sensitivity requirements

## Contact

For questions about models used in ClinScribe AI, please contact the development team.
