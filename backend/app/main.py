from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .database import init_db
from .config import settings
from .routes import documents, tasks, appointments, shopping, reminders, dashboard

# FastAPI App
app = FastAPI(
    title="Persönlicher Alltags- & Dokumenten-Assistent",
    description="KI-gestützter Assistent für Dokumentenverwaltung, Termine und Alltagshilfe",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routen einbinden
app.include_router(documents.router)
app.include_router(tasks.router)
app.include_router(appointments.router)
app.include_router(shopping.router)
app.include_router(reminders.router)
app.include_router(dashboard.router)


@app.on_event("startup")
async def startup_event():
    """Initialisiert Datenbank beim Start."""
    # Verzeichnisse erstellen
    os.makedirs("./data", exist_ok=True)
    os.makedirs(settings.upload_dir, exist_ok=True)

    # Datenbank initialisieren
    init_db()
    print("✅ Datenbank initialisiert")


@app.get("/")
def read_root():
    """Health Check."""
    return {
        "message": "Persönlicher Alltags- & Dokumenten-Assistent API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/api/health")
def health_check():
    """API Health Check."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
