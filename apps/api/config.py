"""
ClinScribe AI — Application Configuration
Uses pydantic-settings for type-safe environment variable management.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Server
    app_name: str = "ClinScribe AI"
    app_env: str = "development"
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000,http://localhost:3001"

    # Database
    database_url: str = "postgresql+asyncpg://clinscribe:clinscribe_dev@localhost:5432/clinscribe_db"
    database_sync_url: str = "postgresql://clinscribe:clinscribe_dev@localhost:5432/clinscribe_db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Authentication
    jwt_secret_key: str = "change-this-to-a-secure-random-string-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 480

    # AI/ML
    asr_provider: str = "demo"
    asr_model_path: str = "./models/indicconformer"
    whisper_model: str = "medium"
    llm_provider: str = "demo"
    llm_api_key: str = ""
    llm_model: str = ""

    # Demo
    demo_mode: bool = True
    demo_data_path: str = "./datasets/synthetic"

    # Audio
    max_audio_duration_seconds: int = 3600
    audio_sample_rate: int = 16000
    temp_audio_dir: str = "./tmp/audio"

    # Privacy
    data_retention_days: int = 90
    enable_audit_log: bool = True

    # Logging
    log_level: str = "INFO"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
