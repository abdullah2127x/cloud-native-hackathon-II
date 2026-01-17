"""Application configuration using Pydantic Settings"""
from pydantic_settings import BaseSettings
from typing import List


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

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
