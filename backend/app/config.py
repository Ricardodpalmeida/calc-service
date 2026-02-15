"""Configuration settings for Calc Service."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment."""
    
    # App
    VERSION: str = "2.0.0"
    DEBUG: bool = False
    
    # API
    API_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Calculator
    DEFAULT_PRECISION: int = 28
    MAX_PRECISION: int = 28
    MAX_EXPONENT: int = 1000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
