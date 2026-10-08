"""
ClinScribe AI — ASR Service Abstraction Layer
Modular speech recognition with pluggable providers.
Primary: AI4Bharat IndicConformer | Fallback: Whisper | Demo: Synthetic
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class ASRSegment:
    """A single transcribed speech segment."""
    text: str
    start_time: float
    end_time: float
    confidence: float
    language: str
    speaker: str = "unknown"


class ASRProvider(ABC):
    """Abstract base class for ASR providers."""

    @abstractmethod
    async def transcribe(self, audio_path: str, language: str = "kn") -> List[ASRSegment]:
        """Transcribe audio file and return segments."""
        pass

    @abstractmethod
    async def transcribe_stream(self, audio_chunk: bytes, language: str = "kn") -> Optional[ASRSegment]:
        """Transcribe a streaming audio chunk."""
        pass

    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """Return list of supported language codes."""
        pass


class IndicConformerProvider(ASRProvider):
    """
    AI4Bharat IndicConformer ASR provider.
    Reference: https://github.com/AI4Bharat/IndicConformerASR
    
    Production implementation would load the actual model.
    Currently configured for architecture demonstration.
    """

    def __init__(self, model_path: str = "./models/indicconformer"):
        self.model_path = model_path
        self.model = None
        self.supported_languages = [
            "kn", "hi", "ta", "te", "ml", "mr", "bn", "gu", "pa", "or",
            "as", "ur", "sa", "en"
        ]
        logger.info(f"IndicConformer provider initialized (model_path: {model_path})")

    async def transcribe(self, audio_path: str, language: str = "kn") -> List[ASRSegment]:
        """
        Transcribe audio using IndicConformer model.
        
        In production: loads and runs the actual IndicConformer model.
        Currently returns structured placeholder for architecture validation.
        """
        logger.info(f"IndicConformer: Transcribing {audio_path} (language: {language})")

        # Production implementation:
        # 1. Load audio file
        # 2. Preprocess (resample to 16kHz, mono)
        # 3. Run IndicConformer inference
        # 4. Post-process and return segments

        raise NotImplementedError(
            "IndicConformer model integration requires model download. "
            "Use DemoASRProvider for hackathon demonstration."
        )

    async def transcribe_stream(self, audio_chunk: bytes, language: str = "kn") -> Optional[ASRSegment]:
        raise NotImplementedError("Streaming not yet implemented for IndicConformer")

    def get_supported_languages(self) -> List[str]:
        return self.supported_languages


class WhisperProvider(ASRProvider):
    """
    OpenAI Whisper fallback ASR provider.
    Used when IndicConformer is unavailable.
    """

    def __init__(self, model_size: str = "medium"):
        self.model_size = model_size
        self.model = None
        self.supported_languages = ["kn", "hi", "ta", "te", "ml", "mr", "en"]
        logger.info(f"Whisper provider initialized (model: {model_size})")

    async def transcribe(self, audio_path: str, language: str = "kn") -> List[ASRSegment]:
        logger.info(f"Whisper: Transcribing {audio_path}")

        # Production implementation:
        # import whisper
        # model = whisper.load_model(self.model_size)
        # result = model.transcribe(audio_path, language=language)

        raise NotImplementedError(
            "Whisper model not loaded. Use DemoASRProvider for hackathon demonstration."
        )

    async def transcribe_stream(self, audio_chunk: bytes, language: str = "kn") -> Optional[ASRSegment]:
        raise NotImplementedError("Streaming not yet implemented for Whisper")

    def get_supported_languages(self) -> List[str]:
        return self.supported_languages


class DemoASRProvider(ASRProvider):
    """
    Demo ASR provider using pre-built synthetic consultation data.
    Provides reliable, deterministic output for hackathon demonstration.
    """

    def __init__(self):
        from demo_data import DEMO_TRANSCRIPT_PRIMARY
        self.demo_transcript = DEMO_TRANSCRIPT_PRIMARY
        self.supported_languages = ["kn-en", "hi-en", "ta-en", "te-en", "ml-en"]
        logger.info("Demo ASR provider initialized")

    async def transcribe(self, audio_path: str, language: str = "kn") -> List[ASRSegment]:
        """Return pre-built demo transcript segments."""
        logger.info(f"Demo ASR: Returning synthetic transcript for {audio_path}")

        # Simulate processing delay for realistic demo
        segments = []
        for seg in self.demo_transcript:
            segments.append(ASRSegment(
                text=seg["text"],
                start_time=seg["start_time"],
                end_time=seg["end_time"],
                confidence=seg["confidence"],
                language=seg["original_language"],
                speaker=seg["speaker"],
            ))

        return segments

    async def transcribe_stream(self, audio_chunk: bytes, language: str = "kn") -> Optional[ASRSegment]:
        """Simulate streaming transcription for demo."""
        return None

    def get_supported_languages(self) -> List[str]:
        return self.supported_languages


# ─── Factory ──────────────────────────────────────────────

def create_asr_provider(provider_name: str, **kwargs) -> ASRProvider:
    """Factory function to create ASR provider instances."""
    providers = {
        "indicconformer": IndicConformerProvider,
        "whisper": WhisperProvider,
        "demo": DemoASRProvider,
    }

    provider_class = providers.get(provider_name.lower())
    if provider_class is None:
        logger.warning(f"Unknown ASR provider '{provider_name}', falling back to demo")
        return DemoASRProvider()

    try:
        return provider_class(**kwargs)
    except Exception as e:
        logger.error(f"Failed to create {provider_name} provider: {e}. Falling back to demo.")
        return DemoASRProvider()
