"""CORS middleware configuration"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings


def configure_cors(app: FastAPI) -> None:
    """Configure CORS middleware for the application"""
    # "null" origin is sent by sandboxed iframes (e.g. ChatKit CDN iframe)
    origins = list(settings.cors_origins) + ["null"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex=r"https://.*\.openai\.com",
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
        max_age=3600,  # Cache preflight requests for 1 hour
    )
