from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from ..database import get_db
from ..models import Appointment
from ..schemas import AppointmentCreate, AppointmentResponse

router = APIRouter(prefix="/api/appointments", tags=["appointments"])


@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    """Erstellt einen neuen Termin."""
    db_appointment = Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(
    upcoming: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Holt alle Termine, optional nur zukünftige."""
    query = db.query(Appointment)

    if upcoming:
        now = datetime.utcnow()
        query = query.filter(Appointment.appointment_date >= now)

    appointments = query.order_by(Appointment.appointment_date.asc()).offset(skip).limit(limit).all()
    return appointments


@router.get("/today", response_model=List[AppointmentResponse])
def get_today_appointments(
    db: Session = Depends(get_db)
):
    """Holt alle heutigen Termine."""
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    appointments = db.query(Appointment).filter(
        Appointment.appointment_date >= today_start,
        Appointment.appointment_date < today_end
    ).order_by(Appointment.appointment_date.asc()).all()

    return appointments


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """Holt einen spezifischen Termin."""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Termin nicht gefunden")
    return appointment


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """Löscht einen Termin."""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Termin nicht gefunden")

    db.delete(appointment)
    db.commit()
    return {"message": "Termin gelöscht"}
