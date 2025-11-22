from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from .models import Base

# Datenbank URL aus Umgebungsvariablen oder Standard
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/assistant.db")

# Engine erstellen
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(DATABASE_URL)

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialisiert die Datenbank und erstellt alle Tabellen."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency für FastAPI, um DB-Sessions zu erhalten."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
