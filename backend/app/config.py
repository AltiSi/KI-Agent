from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Keys
    anthropic_api_key: str

    # Datenbank
    database_url: str = "sqlite:///./data/assistant.db"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Upload-Verzeichnis
    upload_dir: str = "./uploads"

    # CORS
    cors_origins: list = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
