from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime

from ..database import get_db
from ..models import Document, Task, Appointment
from ..schemas import DocumentResponse, TaskCreate, AppointmentCreate
from ..services.document_processor import document_processor
from ..services.ai_service import ai_service
from ..config import settings

router = APIRouter(prefix="/api/documents", tags=["documents"])

# Upload-Verzeichnis erstellen falls nicht vorhanden
os.makedirs(settings.upload_dir, exist_ok=True)


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Lädt ein Dokument hoch und analysiert es automatisch mit KI.
    """

    # Datei speichern
    file_path = os.path.join(settings.upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Text extrahieren
    document_text = document_processor.extract_text(file_path, file.filename)

    if not document_text:
        raise HTTPException(status_code=400, detail="Konnte keinen Text aus dem Dokument extrahieren.")

    # KI-Analyse
    analysis = ai_service.analyze_document(document_text, file.filename)

    # Dokument in Datenbank speichern
    db_document = Document(
        title=file.filename,
        filename=file.filename,
        file_path=file_path,
        category=analysis.get("category", "Sonstiges"),
        summary=analysis.get("summary", ""),
        important_info=analysis.get("important_info", ""),
        next_steps="\n".join(analysis.get("next_steps", []))
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    # Automatisch Aufgaben erstellen
    for task_data in analysis.get("tasks", []):
        task = Task(
            title=task_data.get("title", ""),
            priority=task_data.get("priority", "mittel"),
            due_date=datetime.fromisoformat(task_data["due_date"]) if task_data.get("due_date") else None,
            document_id=db_document.id
        )
        db.add(task)

    # Automatisch Termine erstellen
    for appointment_data in analysis.get("appointments", []):
        appointment = Appointment(
            title=appointment_data.get("title", ""),
            description=appointment_data.get("description"),
            appointment_date=datetime.fromisoformat(appointment_data["date"]),
            location=appointment_data.get("location"),
            document_id=db_document.id
        )
        db.add(appointment)

    db.commit()

    return db_document


@router.get("/", response_model=List[DocumentResponse])
def get_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Holt alle Dokumente.
    """
    documents = db.query(Document).order_by(Document.created_at.desc()).offset(skip).limit(limit).all()
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Holt ein spezifisches Dokument.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Dokument nicht gefunden")
    return document


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Löscht ein Dokument (und zugehörige Datei).
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Dokument nicht gefunden")

    # Datei löschen
    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    # Aus Datenbank löschen
    db.delete(document)
    db.commit()

    return {"message": "Dokument gelöscht"}
