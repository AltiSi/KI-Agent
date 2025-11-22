from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # AI Provider: "claude" oder "ollama"
    ai_provider: str = "ollama"  # Standard: Ollama (kostenlos!)

    # API Keys (nur für Claude nötig)
    anthropic_api_key: Optional[str] = "dummy-key"

    # Ollama Settings
    ollama_url: str = "http://localhost:11434/api/generate"
    ollama_model: str = "llama3.2"  # oder "mistral"

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
