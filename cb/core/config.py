"""Configuration management for CB Algorithm Tutor."""

import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI Configuration
    openai_api_key: str
    model_name: str = "gpt-4-turbo-preview"
    max_tokens: int = 2000
    temperature: float = 0.7
    
    # Database Configuration
    database_url: str = "sqlite:///cb_tutor.db"
    
    # Application Configuration
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


# Global settings instance
settings = get_settings()