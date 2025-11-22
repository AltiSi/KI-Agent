"""
AI Service Factory - wählt automatisch zwischen Claude und Ollama.
"""

from ..config import settings


def get_ai_service():
    """
    Gibt den konfigurierten AI Service zurück.

    Wenn AI_PROVIDER=ollama (Standard) → Ollama (kostenlos)
    Wenn AI_PROVIDER=claude → Claude API
    """

    if settings.ai_provider.lower() == "ollama":
        from .ollama_service import ollama_ai_service
        return ollama_ai_service
    elif settings.ai_provider.lower() == "claude":
        from .ai_service import ai_service
        return ai_service
    else:
        # Fallback zu Ollama
        from .ollama_service import ollama_ai_service
        return ollama_ai_service


# Singleton - wird automatisch den richtigen Service nutzen
ai = get_ai_service()
