from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Reminder
from ..schemas import ReminderCreate, ReminderResponse

router = APIRouter(prefix="/api/reminders", tags=["reminders"])


@router.post("/", response_model=ReminderResponse)
def create_reminder(
    reminder: ReminderCreate,
    db: Session = Depends(get_db)
):
    """Erstellt eine neue Erinnerung."""
    db_reminder = Reminder(**reminder.model_dump())
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder


@router.get("/", response_model=List[ReminderResponse])
def get_reminders(
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Holt alle Erinnerungen."""
    query = db.query(Reminder)

    if active_only:
        query = query.filter(Reminder.active == True)

    reminders = query.order_by(Reminder.reminder_time.asc()).offset(skip).limit(limit).all()
    return reminders


@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder(
    reminder_id: int,
    db: Session = Depends(get_db)
):
    """Holt eine spezifische Erinnerung."""
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Erinnerung nicht gefunden")
    return reminder


@router.patch("/{reminder_id}/toggle")
def toggle_reminder(
    reminder_id: int,
    db: Session = Depends(get_db)
):
    """Aktiviert/Deaktiviert eine Erinnerung."""
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Erinnerung nicht gefunden")

    reminder.active = not reminder.active
    db.commit()
    db.refresh(reminder)
    return reminder


@router.delete("/{reminder_id}")
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db)
):
    """Löscht eine Erinnerung."""
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Erinnerung nicht gefunden")

    db.delete(reminder)
    db.commit()
    return {"message": "Erinnerung gelöscht"}
