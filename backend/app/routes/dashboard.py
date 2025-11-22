from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..database import get_db
from ..models import Task, Appointment
from ..schemas import DashboardResponse
from ..services.ai_service import ai_service

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db)
):
    """
    Holt Dashboard-Übersicht mit:
    - Anstehenden Aufgaben
    - Heutigen Terminen
    - KI-generierter Tageszusammenfassung
    """

    # Offene Aufgaben mit Frist in den nächsten 7 Tagen
    next_week = datetime.utcnow() + timedelta(days=7)
    upcoming_tasks = db.query(Task).filter(
        Task.completed == False,
        Task.due_date <= next_week
    ).order_by(Task.due_date.asc()).limit(10).all()

    # Heutige Termine
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    today_appointments = db.query(Appointment).filter(
        Appointment.appointment_date >= today_start,
        Appointment.appointment_date < today_end
    ).order_by(Appointment.appointment_date.asc()).all()

    # Anstehende Termine (nächste 7 Tage)
    upcoming_appointments = db.query(Appointment).filter(
        Appointment.appointment_date >= datetime.utcnow(),
        Appointment.appointment_date <= next_week
    ).order_by(Appointment.appointment_date.asc()).limit(10).all()

    # Zähler
    pending_tasks_count = db.query(Task).filter(Task.completed == False).count()
    today_appointments_count = len(today_appointments)

    # KI-generierte Tageszusammenfassung
    tasks_data = [
        {
            "title": task.title,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None
        }
        for task in upcoming_tasks
    ]

    appointments_data = [
        {
            "title": apt.title,
            "date": apt.appointment_date.isoformat(),
            "location": apt.location
        }
        for apt in today_appointments
    ]

    daily_summary = ai_service.get_daily_summary(tasks_data, appointments_data)

    return DashboardResponse(
        upcoming_tasks=upcoming_tasks,
        upcoming_appointments=upcoming_appointments,
        daily_summary=daily_summary,
        pending_tasks_count=pending_tasks_count,
        today_appointments_count=today_appointments_count
    )
