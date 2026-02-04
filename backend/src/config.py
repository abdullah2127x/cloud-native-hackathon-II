"""Application configuration using Pydantic Settings"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
import json


class Settings(BaseSettings):
    """Application settings"""

    # Database
    database_url: str = "sqlite:///./test.db"

    # Better Auth
    better_auth_url: str = "http://localhost:3000"
    better_auth_secret: str = "your-secret-key-change-in-production"

    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]

    # JWT - Better Auth uses EdDSA (Ed25519) by default, audience is BASE_URL
    jwt_algorithm: str = "EdDSA"
    jwt_audience: str = "http://localhost:3000"

    # Application
    app_name: str = "Todo Backend"
    debug: bool = False

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from JSON string or list"""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
